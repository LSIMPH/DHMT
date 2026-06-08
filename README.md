# Monocular Depth Estimation - Hướng Dẫn Dành Cho Người Mới

Dự án này giúp ước lượng độ sâu của một bức ảnh 2D thông thường (Monocular Depth Estimation) bằng cách sử dụng trí tuệ nhân tạo (mô hình MiDaS).

Dưới đây là hướng dẫn chi tiết từng bước để bất kỳ ai, kể cả người chưa từng lập trình Python hay Git, cũng có thể cài đặt và chạy được chương trình.

---

## Bước 1: Chuẩn bị máy tính (Cài đặt Python)

Nếu máy tính của bạn chưa có Python, bạn cần cài đặt nó trước tiên.
1. Truy cập trang web chính thức của Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Tải bản cài đặt mới nhất cho Windows.
3. **Rất quan trọng:** Khi chạy file cài đặt, hãy đảm bảo bạn **TÍCH CHỌN ô "Add Python to PATH"** ở màn hình đầu tiên trước khi nhấn nút "Install Now".

## Bước 2: Tải mã nguồn dự án về máy

Để chạy được chương trình, bạn cần mang thư mục chứa mã nguồn này về máy tính của mình. Bạn có thể làm theo 1 trong 2 cách sau:

**Cách 1: Tải file nén (Dễ nhất - Không cần cài thêm phần mềm)**
1. Lên trang GitHub chứa mã nguồn này.
2. Bấm vào nút màu xanh lá cây có chữ **"<> Code"** ở góc phải.
3. Chọn **"Download ZIP"**.
4. Sau khi tải xong, hãy **giải nén** file ZIP đó ra một thư mục trên máy tính của bạn.

**Cách 2: Sử dụng Git clone (Dành cho người đã cài đặt Git)**
Mở Terminal/PowerShell ở thư mục bạn muốn lưu dự án và gõ lệnh:
```powershell
git clone <đường-dẫn-repo-của-bạn>
```
*(Lưu ý: Thay `<đường-dẫn-repo-của-bạn>` bằng link GitHub của bạn)*

## Bước 3: Mở cửa sổ dòng lệnh (Terminal)

1. Mở thư mục mà bạn vừa giải nén (hoặc vừa clone về). Hãy đảm bảo bạn đang nhìn thấy file có tên là `monocular_depth_estimation.py`.
2. Nhấn chuột phải vào khoảng trống bất kỳ trong thư mục đó, chọn **"Open in Terminal"** (Mở trong Terminal) hoặc **"Open PowerShell window here"**.

## Bước 4: Cài đặt môi trường và thư viện

Chúng ta sẽ tạo một "môi trường ảo" để tải các thư viện AI cần thiết mà không làm ảnh hưởng đến máy tính của bạn. Copy từng dòng lệnh dưới đây, dán vào Terminal vừa mở và nhấn **Enter**:

**Lệnh 1: Tạo môi trường ảo**
```powershell
python -m venv .venv
```
*(Chờ khoảng vài giây, bạn sẽ thấy một thư mục mới có tên là `.venv` xuất hiện).*

**Lệnh 2: Cài đặt các thư viện**
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```
*(Quá trình này có thể mất vài phút tùy thuộc vào tốc độ mạng của bạn để tải các thư viện xử lý ảnh và AI. Hãy chờ cho đến khi hoàn thành 100%).*

## Bước 5: Chạy chương trình

Bây giờ mọi thứ đã sẵn sàng. Bạn chạy chương trình bằng lệnh sau. Trong ví dụ này, chúng ta sẽ xử lý bức ảnh có tên `image.jpg`:

```powershell
.venv\Scripts\python.exe monocular_depth_estimation.py --image image.jpg
```

**Một số lưu ý quan trọng khi chạy:**
1. **Thay đổi ảnh:** Nếu bạn muốn thử với bức ảnh khác, hãy chép ảnh đó vào cùng thư mục này và sửa chữ `image.jpg` trong lệnh trên thành tên ảnh của bạn (ví dụ: `--image anh-cua-toi.png`).
2. **Tải mô hình AI lần đầu:** Trong lần chạy đầu tiên, chương trình sẽ tự động tải mô hình AI từ Internet về. Sẽ có một thông báo bằng tiếng Anh hỏi bạn có tin tưởng kho lưu trữ GitHub này không *(Do you trust this repository...)*. Bạn chỉ cần gõ chữ **`y`** rồi nhấn **Enter** là được.
3. **Tương tác với ảnh:** Khi cửa sổ hình ảnh hiện lên, bạn có thể **click chuột** vào các điểm trên ảnh để xem Terminal hiển thị khoảng cách (độ sâu) của điểm đó.
4. **Thoát chương trình:** Để đóng chương trình, hãy click chuột vào cửa sổ hình ảnh rồi bấm phím **`Esc`** hoặc phím **`q`**.

Chúc bạn thành công!
