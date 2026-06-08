#!/usr/bin/env python3
"""Monocular Depth Estimation using MiDaS.

Tieu chuong trinh:
- Doc EXIF co ban tu anh
- Su dung MiDaS de uoc luong do sau tuyet doi/tuong doi
- Chuan hoa ma tran depth ve uint8 [0, 255]
- Hien thi depth map bang color map
- Bat su kien click chuot de in gia tri depth tai diem (x, y)

Chay vi du:
    python monocular_depth_estimation.py --image path/to/image.jpg
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

try:
    import cv2
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "Thieu thu vien 'opencv-python'. Hay cai dat truoc: pip install -r requirements.txt"
    ) from exc

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "Thieu thu vien 'numpy'. Hay cai dat truoc: pip install -r requirements.txt"
    ) from exc

try:
    from PIL import ExifTags, Image
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "Thieu thu vien 'Pillow'. Hay cai dat truoc: pip install -r requirements.txt"
    ) from exc

try:
    import torch
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "Thieu thu vien 'torch'. Hay cai dat truoc: pip install torch torchvision"
    ) from exc


@dataclass
class DepthResult:
    depth_raw: np.ndarray  # Ma tran Z goc tu mo hinh, chua chuan hoa
    depth_uint8: np.ndarray  # Depth da chuan hoa ve [0, 255]
    depth_color: np.ndarray  # Depth da gan color map


class DepthAppState:
    def __init__(self) -> None:
        self.original_bgr: Optional[np.ndarray] = None
        self.depth_raw: Optional[np.ndarray] = None  # Luu tru Z thuc te (da nghich dao)
        self.disparity_raw: Optional[np.ndarray] = None # Luu tru disparity goc tu MiDaS
        self.side_by_side: Optional[np.ndarray] = None
        self.original_width: int = 0
        self.original_height: int = 0


def get_exif(image_path: str) -> Dict[str, Any]:
    """Doc EXIF co ban tu anh.

    Pillow tra ve mot dictionary voi key la ma so EXIF. Ta doi sang ten
    thong dung de de doc hon.
    """
    exif_data: Dict[str, Any] = {}
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if not exif:
                return exif_data

            tag_map = {v: k for k, v in ExifTags.TAGS.items()}
            for key_id, value in exif.items():
                tag_name = ExifTags.TAGS.get(key_id, str(key_id))
                exif_data[tag_name] = value

            # Bổ sung vài thông số cơ bản nếu có.
            # FocalLength / FNumber thuong co dang tuple (num, den).
            if "FocalLength" in exif_data and isinstance(exif_data["FocalLength"], tuple):
                num, den = exif_data["FocalLength"]
                if den:
                    exif_data["FocalLength"] = num / den
            if "FNumber" in exif_data and isinstance(exif_data["FNumber"], tuple):
                num, den = exif_data["FNumber"]
                if den:
                    exif_data["FNumber"] = num / den

            # Image size khong phai EXIF chuan, nhung rat huu ich khi in ra console.
            exif_data["ImageSize"] = img.size
    except FileNotFoundError:
        raise
    except Exception as exc:
        print(f"[Canh bao] Khong the doc EXIF: {exc}")

    return exif_data


def print_exif_summary(exif_data: Dict[str, Any]) -> None:
    if not exif_data:
        print("EXIF: Khong co metadata hoac anh khong chua EXIF.")
        return

    print("EXIF co ban:")
    for key in ["Make", "Model", "FocalLength", "FNumber", "ExposureTime", "ISOSpeedRatings", "ImageSize"]:
        if key in exif_data:
            print(f"  - {key}: {exif_data[key]}")


def load_image_bgr(image_path: str) -> np.ndarray:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Khong tim thay file anh: {image_path}")

    image_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError(f"Khong the doc anh: {image_path}")
    return image_bgr


def load_midas_model(model_type: str = "MiDaS_small") -> Tuple[torch.nn.Module, Any, torch.device]:
    """Tai mo hinh MiDaS qua torch.hub.

    - MiDaS_small: nhe, chay nhanh tren CPU.
    - DPT_Hybrid / DPT_Large: nang hon, chat luong cao hon.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Dang tai model '{model_type}' tren device: {device}")
    model = torch.hub.load("intel-isl/MiDaS", model_type, pretrained=True)
    model.to(device)
    model.eval()

    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    if model_type == "MiDaS_small":
        transform = transforms.small_transform
    else:
        transform = transforms.dpt_transform

    return model, transform, device


@torch.no_grad()
def estimate_depth(
    image_bgr: np.ndarray,
    model: torch.nn.Module,
    transform: Any,
    device: torch.device,
) -> DepthResult:
    """Uoc luong depth map tu anh dau vao.

    Quy trinh tong quat:
    1. Chuyen BGR sang RGB vi MiDaS mong doi anh mau theo thoi quen CV/PIL.
    2. Dung transform cua MiDaS de resize / normalize / tao tensor.
    3. Chay forward pass qua mo hinh de lay ra ma tran Z.
    4. Noi suy (interpolate) map do sau ve dung kich thuoc anh goc.
    5. Chuan hoa ve [0, 255] de hien thi.
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    input_batch = transform(image_rgb).to(device)

    # input_batch co shape: [1, 3, H, W]
    prediction = model(input_batch)

    # prediction la tensor depth/relative disparity o do phan giai thap hon.
    # Ta can dua no ve kich thuoc anh goc bang noi suy song tuyen.
    prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size=image_rgb.shape[:2],
        mode="bicubic",
        align_corners=False,
    ).squeeze()

    # MiDaS tra ve Disparity (Nghich dao cua do sau). Gia tri cang lon tuc la cang gan.
    disparity_raw = prediction.cpu().numpy().astype(np.float32)

    # De tinh Do sau Z (Depth) thuc te (cang xa gia tri cang lon), ta lay nghich dao:
    # Z = 1 / disparity (Cong them 1e-6 de tranh chia cho 0)
    depth_raw = 1.0 / (disparity_raw + 1e-6)

    # Chuan hoa DISPARITY de ve anh (Theo quy uoc CV: Gan = Sang/Vang, Xa = Toi/Tim)
    disp_min = float(np.min(disparity_raw))
    disp_max = float(np.max(disparity_raw))

    if disp_max - disp_min < 1e-8:
        depth_uint8 = np.zeros_like(disparity_raw, dtype=np.uint8)
    else:
        disp_norm = (disparity_raw - disp_min) / (disp_max - disp_min)
        depth_uint8 = (disp_norm * 255.0).clip(0, 255).astype(np.uint8)

    depth_color = cv2.applyColorMap(depth_uint8, cv2.COLORMAP_INFERNO)

    return DepthResult(depth_raw=depth_raw, depth_uint8=depth_uint8, depth_color=depth_color)


def build_side_by_side(original_bgr: np.ndarray, depth_color: np.ndarray) -> np.ndarray:
    """Ghep anh goc va depth map theo chieu ngang.

    Neu kich thuoc khac nhau, depth_color duoc resize ve dung size anh goc
    de click chuot va doi chieu toa do khong bi lech.
    """
    h, w = original_bgr.shape[:2]
    depth_resized = cv2.resize(depth_color, (w, h), interpolation=cv2.INTER_CUBIC)
    return np.hstack([original_bgr, depth_resized])


def on_mouse(event: int, x: int, y: int, flags: int, state: DepthAppState) -> None:
    """Mouse callback: click vao anh de in depth Z tai diem (x, y)."""
    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if state.depth_raw is None or state.original_width == 0:
        return

    if x < state.original_width:
        ix, iy = x, y
        if iy >= state.depth_raw.shape[0] or ix >= state.depth_raw.shape[1]:
            return
        z_value = float(state.depth_raw[iy, ix])
        print(f"Click ({ix}, {iy}) -> Do sau Z (tuong doi) = {z_value:.6f}")
    else:
        # Nua ben phai la depth map. Tru toa do ve khung anh goc.
        ix = x - state.original_width
        iy = y
        if iy >= state.depth_raw.shape[0] or ix >= state.depth_raw.shape[1]:
            return
        z_value = float(state.depth_raw[iy, ix])
        print(f"Click depth-map ({ix}, {iy}) -> Do sau Z (tuong doi) = {z_value:.6f}")


def run_app(image_path: str, model_type: str = "MiDaS_small") -> None:
    image_bgr = load_image_bgr(image_path)
    exif_data = get_exif(image_path)
    print_exif_summary(exif_data)

    model, transform, device = load_midas_model(model_type=model_type)
    depth_result = estimate_depth(image_bgr, model, transform, device)

    comparison = build_side_by_side(image_bgr, depth_result.depth_color)

    # Luu vao state de callback doc duoc depth matrix.
    state = DepthAppState()
    state.original_bgr = image_bgr
    state.depth_raw = depth_result.depth_raw
    state.side_by_side = comparison
    state.original_height, state.original_width = image_bgr.shape[:2]

    window_name = "Monocular Depth Estimation - Original | Depth"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, on_mouse, state)

    try:
        while True:
            # Khi nguoi dung dong cua so bang nut X, OpenCV se danh dau cua so
            # khong con visible. Neu khong kiem tra dieu nay, vong lap se tiep
            # tuc goi imshow va cua so co the bi tao lai.
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

            cv2.imshow(window_name, comparison)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monocular Depth Estimation voi MiDaS")
    parser.add_argument("--image", required=True, help="Duong dan toi file anh dau vao")
    parser.add_argument(
        "--model",
        default="MiDaS_small",
        choices=["MiDaS_small", "DPT_Hybrid", "DPT_Large"],
        help="Lua chon mo hinh MiDaS",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_app(args.image, args.model)
        return 0
    except FileNotFoundError as exc:
        print(f"[Loi] {exc}")
        return 1
    except ValueError as exc:
        print(f"[Loi] {exc}")
        return 1
    except KeyboardInterrupt:
        print("Da dung chuong trinh.")
        return 0
    except Exception as exc:
        print(f"[Loi khong xac dinh] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
