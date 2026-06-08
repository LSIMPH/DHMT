# BÁO CÁO HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH

## Monocular Depth Estimation (Ước Lượng Độ Sâu Ảnh Đơn)

---

> **Môn học:** Đồ Họa Máy Tính  
> **Sinh viên thực hiện:** Nguyễn Hoàng Duy  
> **Ngày:** 08/06/2026

---

## 1. GIỚI THIỆU CHƯƠNG TRÌNH

Chương trình **Monocular Depth Estimation** sử dụng mô hình AI **MiDaS** (Intel ISL) để ước lượng độ sâu không gian 3D từ một bức ảnh 2D thông thường — không cần camera đặc biệt hay cặp ảnh stereo.

### Tính năng chính:
| Tính năng | Mô tả |
|-----------|-------|
| **Đọc siêu dữ liệu ảnh (EXIF)** | Hiển thị thông tin camera như tiêu cự, khẩu độ, ISO... |
| **Ước lượng độ sâu** | Dùng mô hình MiDaS để tính ma trận độ sâu tương đối |
| **Hiển thị bản đồ màu** | Dùng color map INFERNO: vùng **sáng/vàng = gần**, **tối/tím = xa** |
| **So sánh trực quan** | Hiển thị ảnh gốc và depth map cạnh nhau trong cùng một cửa sổ |
| **Tương tác chuột** | Click vào bất kỳ điểm nào trên ảnh để xem giá trị độ sâu tại điểm đó |

### Các mô hình AI hỗ trợ:
- `MiDaS_small` – Nhẹ, nhanh, phù hợp máy không có GPU *(mặc định)*
- `DPT_Hybrid` – Chất lượng tốt hơn, cần nhiều RAM hơn
- `DPT_Large` – Chất lượng cao nhất, cần GPU mạnh

---

## 2. YÊU CẦU HỆ THỐNG

| Thành phần | Yêu cầu tối thiểu |
|------------|-------------------|
| **Hệ điều hành** | Windows 10/11 (64-bit) |
| **Python** | Phiên bản **3.9** trở lên |
| **RAM** | Tối thiểu **4 GB** (khuyến nghị 8 GB) |
| **Dung lượng ổ cứng** | ~3 GB (cho thư viện + mô hình AI) |
| **Kết nối Internet** | Cần có khi tải mô hình lần đầu |
| **GPU** | Không bắt buộc – CPU là đủ để chạy `MiDaS_small` |

---

## 3. CÀI ĐẶT PYTHON (Bỏ qua nếu đã có Python)

1. Truy cập: **https://www.python.org/downloads/**
2. Nhấn **"Download Python 3.x.x"** (phiên bản mới nhất).
3. Chạy file cài đặt vừa tải về.

> ⚠️ **RẤT QUAN TRỌNG:** Ở màn hình đầu tiên của trình cài đặt, hãy **TÍCH CHỌN ô "Add Python to PATH"** trước khi nhấn **"Install Now"**.

   ```
   ┌─────────────────────────────────────────┐
   │  Install Python 3.x.x                   │
   │                                         │
   │  ☑ Add Python to PATH   ← TÍCH VÀO ĐÂY │
   │                                         │
   │  [ Install Now ]                        │
   └─────────────────────────────────────────┘
   ```

4. Sau khi cài xong, mở **PowerShell** và kiểm tra bằng lệnh:
   ```powershell
   python --version
   ```
   Kết quả phải hiện ra như: `Python 3.12.x`

---

## 4. TẢI MÃ NGUỒN DỰ ÁN

Có 2 cách để lấy mã nguồn về máy:

### Cách 1: Tải file ZIP (Đơn giản nhất, không cần cài thêm gì)

1. Truy cập trang GitHub của dự án.
2. Nhấn vào nút màu xanh lá **`<> Code`** ở góc trên bên phải.
3. Chọn **"Download ZIP"**.
4. Sau khi tải xong, **nhấp chuột phải** vào file ZIP và chọn **"Extract All..."**.
5. Chọn vị trí giải nén (ví dụ: `C:\DHMT\`) rồi nhấn **"Extract"**.

### Cách 2: Dùng Git clone (Nếu đã cài Git)

```powershell
git clone https://github.com/<username>/DHMT.git
cd DHMT
```

---

## 5. MỞ TERMINAL TẠI THƯ MỤC DỰ ÁN

Sau khi có thư mục dự án, bạn cần mở Terminal **ngay tại thư mục đó**:

**Cách nhanh nhất:**
1. Mở thư mục dự án bằng File Explorer.
2. Đảm bảo bạn nhìn thấy file `monocular_depth_estimation.py` bên trong.
3. Nhấn **chuột phải** vào khoảng trống bất kỳ trong thư mục.
4. Chọn **"Open in Terminal"** hoặc **"Open PowerShell window here"**.

---

## 6. CÀI ĐẶT MÔI TRƯỜNG VÀ THƯ VIỆN

Trong cửa sổ Terminal vừa mở, chạy lần lượt **2 lệnh** sau:

### Lệnh 1: Tạo môi trường ảo Python

```powershell
python -m venv .venv
```

> Chờ vài giây. Một thư mục tên `.venv` sẽ xuất hiện trong thư mục dự án.

### Lệnh 2: Cài đặt các thư viện cần thiết

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> ⏳ **Quá trình này có thể mất từ 5–15 phút** tùy tốc độ mạng, vì cần tải các thư viện AI nặng như `torch`, `torchvision`, `opencv`, `Pillow`, `timm`. Hãy chờ đến khi Terminal hiển thị thông báo hoàn thành.

**Danh sách thư viện sẽ được cài:**

| Thư viện | Vai trò |
|----------|---------|
| `torch` | Framework AI (PyTorch) – chạy mô hình MiDaS |
| `torchvision` | Hỗ trợ xử lý ảnh cho PyTorch |
| `opencv-python` | Đọc/ghi ảnh, hiển thị cửa sổ, xử lý màu sắc |
| `Pillow` | Đọc thông tin EXIF từ ảnh JPEG |
| `numpy` | Xử lý ma trận số học |
| `timm` | Thư viện mô hình thị giác máy tính (PyTorch Image Models) |

---

## 7. CHẠY CHƯƠNG TRÌNH

### Cú pháp cơ bản:

```powershell
.venv\Scripts\python.exe monocular_depth_estimation.py --image <tên_ảnh>
```

### Ví dụ cụ thể (dùng ảnh có sẵn trong thư mục):

```powershell
.venv\Scripts\python.exe monocular_depth_estimation.py --image image.jpg
```

Bạn cũng có thể thử với các ảnh mẫu khác đi kèm dự án:

```powershell
.venv\Scripts\python.exe monocular_depth_estimation.py --image image1.jpg
.venv\Scripts\python.exe monocular_depth_estimation.py --image image2.jpg
.venv\Scripts\python.exe monocular_depth_estimation.py --image image3.jpg
.venv\Scripts\python.exe monocular_depth_estimation.py --image image4.jpg
```

### Chọn mô hình AI khác (tùy chọn):

```powershell
# Mô hình chất lượng cao hơn (cần nhiều RAM, chạy chậm hơn)
.venv\Scripts\python.exe monocular_depth_estimation.py --image image.jpg --model DPT_Hybrid
```

---

## 8. LẦN CHẠY ĐẦU TIÊN – TẢI MÔ HÌNH AI

Khi chạy lần đầu, chương trình sẽ tự động tải mô hình AI `MiDaS_small` từ Internet về máy tính. Sẽ có thông báo hỏi:

```
Do you trust this repository? [y/N]
```

**Gõ chữ `y` rồi nhấn Enter** để xác nhận tin tưởng kho lưu trữ và tiếp tục tải.

> Sau lần đầu, mô hình sẽ được lưu lại vào bộ nhớ cache trên máy. Những lần chạy tiếp theo sẽ **không cần tải lại** và sẽ khởi động nhanh hơn.

---

## 9. SỬ DỤNG CHƯƠNG TRÌNH

Sau khi chương trình chạy thành công, một **cửa sổ hình ảnh** sẽ xuất hiện hiển thị hai ảnh cạnh nhau:

```
┌────────────────────────────────────────────────┐
│  Monocular Depth Estimation - Original | Depth │
├────────────────────┬───────────────────────────┤
│                    │                           │
│   ẢNH GỐC          │   BẢN ĐỒ ĐỘ SÂU (Màu)    │
│   (Original)       │   (Depth Map)             │
│                    │                           │
│                    │  🟡 Vàng/Sáng = Gần        │
│                    │  🟣 Tím/Tối  = Xa          │
│                    │                           │
└────────────────────┴───────────────────────────┘
```

### Các thao tác tương tác:

| Thao tác | Kết quả |
|----------|---------|
| **Click chuột trái** vào ảnh gốc (nửa trái) | Terminal in ra giá trị độ sâu Z tại điểm click |
| **Click chuột trái** vào depth map (nửa phải) | Terminal in ra giá trị độ sâu Z tương ứng |
| Nhấn phím **`Esc`** hoặc **`q`** | Thoát khỏi chương trình |
| Nhấn nút **`X`** để đóng cửa sổ | Thoát khỏi chương trình |

### Ví dụ kết quả khi click chuột trên Terminal:

```
EXIF co ban:
  - Make: Apple
  - Model: iPhone 14 Pro
  - FocalLength: 6.86
  - FNumber: 1.78
  - ImageSize: (4032, 3024)

Dang tai model 'MiDaS_small' tren device: cpu
Click (312, 245) -> Do sau Z (tuong doi) = 1.234567
Click depth-map (156, 200) -> Do sau Z (tuong doi) = 2.891023
```

> **Lưu ý về giá trị Z:** Đây là giá trị độ sâu **tương đối** (không phải đơn vị mét thực tế). Giá trị **nhỏ hơn = gần hơn**, giá trị **lớn hơn = xa hơn** so với camera.

---

## 10. DỮ LIỆU ẢNH MẪU KÈM THEO

Dự án bao gồm các ảnh mẫu để kiểm thử trực tiếp:

| File ảnh | Dung lượng |
|----------|------------|
| `image.jpg` | ~11.6 MB |
| `image1.jpg` | ~12.8 MB |
| `image2.jpg` | ~12.2 MB |
| `image3.jpg` | ~24.0 MB |
| `image4.jpg` | ~6.6 MB |

Bạn cũng có thể **thêm ảnh của riêng mình** bằng cách chép file ảnh (`.jpg`, `.png`) vào thư mục dự án và thay tên ảnh trong lệnh chạy.

---

## 11. XỬ LÝ LỖI THƯỜNG GẶP

### ❌ Lỗi: `'python' is not recognized as an internal or external command`
**Nguyên nhân:** Python chưa được thêm vào PATH.  
**Giải pháp:** Cài lại Python và **đảm bảo tích chọn "Add Python to PATH"** (xem Bước 3).

---

### ❌ Lỗi: `No module named 'torch'` hoặc thiếu thư viện khác
**Nguyên nhân:** Chưa cài thư viện hoặc đang dùng sai môi trường Python.  
**Giải pháp:** Chạy lại lệnh cài thư viện:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

### ❌ Lỗi: `FileNotFoundError: Khong tim thay file anh`
**Nguyên nhân:** Tên file ảnh bị sai hoặc ảnh không nằm trong thư mục dự án.  
**Giải pháp:** Kiểm tra lại tên file và đảm bảo ảnh nằm **cùng thư mục** với `monocular_depth_estimation.py`.

---

### ❌ Chương trình chạy rất chậm
**Nguyên nhân:** Máy không có GPU, đang xử lý trên CPU.  
**Giải pháp:** Đây là bình thường với máy không có GPU NVIDIA. Hãy kiên nhẫn chờ – thường mất 10–60 giây tùy cấu hình máy.

---

## 12. CẤU TRÚC THƯ MỤC DỰ ÁN

```
DHMT/
├── monocular_depth_estimation.py   # File mã nguồn chính
├── requirements.txt                # Danh sách thư viện cần cài
├── README.md                       # Hướng dẫn nhanh
├── HUONG_DAN_CAI_DAT.md            # File báo cáo này
├── image.jpg                       # Ảnh mẫu 1
├── image1.jpg                      # Ảnh mẫu 2
├── image2.jpg                      # Ảnh mẫu 3
├── image3.jpg                      # Ảnh mẫu 4
└── image4.jpg                      # Ảnh mẫu 5
```

---

## 13. TÓM TẮT LỆNH NHANH

Sau khi đã cài đặt xong (chỉ cần làm 1 lần), mỗi lần chạy chương trình chỉ cần:

```powershell
# 1. Mở Terminal tại thư mục dự án
# 2. Chạy lệnh:
.venv\Scripts\python.exe monocular_depth_estimation.py --image image.jpg
```

---

*Tài liệu này được tạo để hỗ trợ việc cài đặt và kiểm tra chương trình trên máy tính của giảng viên.*
