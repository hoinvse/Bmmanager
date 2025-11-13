# 🚀 BM Manager Pro - Hướng dẫn sử dụng

## 📋 Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt và khởi chạy](#cài-đặt-và-khởi-chạy)
3. [Giao diện chính](#giao-diện-chính)
4. [Chức năng chính](#chức-năng-chính)
5. [Hướng dẫn chi tiết](#hướng-dẫn-chi-tiết)
6. [Các phím tắt](#các-phím-tắt)
7. [Lưu ý quan trọng](#lưu-ý-quan-trọng)

---

## 🎯 Giới thiệu

**BM Manager Pro** là ứng dụng quản lý Business Manager Facebook chuyên nghiệp, giúp bạn:
- ✅ Quản lý thông tin BM (Business Manager) một cách có tổ chức
- 📁 Phân loại dữ liệu theo thư mục
- 🔗 Lưu trữ nhiều link (tối đa 3 link) cho mỗi BM
- 📝 Thêm ghi chú và nhận xét
- 🔍 Lọc và tìm kiếm dữ liệu nhanh chóng
- 📋 Import/Export dữ liệu dễ dàng

---

## 💻 Cài đặt và khởi chạy

### Yêu cầu hệ thống
- Python 3.7 trở lên
- Thư viện tkinter (thường có sẵn với Python)

### Cài đặt
```bash
# Clone hoặc tải code về
# Không cần cài đặt thêm thư viện nào

# Chạy ứng dụng
python bm_manager.py
```

### Cấu trúc thư mục
```
bm_manager.py
bm_data/
  ├── default/
  │   └── bm_data.json
  ├── folder1/
  │   └── bm_data.json
  └── folder2/
      └── bm_data.json
```

---

## 🎨 Giao diện chính

Ứng dụng có 2 tab chính:

### 1. 📊 Tab Quản lý
- **Header**: Tiêu đề và nút chuyển tab
- **Quản lý thư mục**: Tạo, xóa, đổi tên, di chuyển giữa các thư mục
- **Bảng dữ liệu**: Hiển thị danh sách BM với đầy đủ thông tin
- **Menu chuột phải**: Truy cập nhanh các chức năng

### 2. 🔍 Tab Lọc Link
- Lọc link theo danh sách BmID
- Hiển thị kết quả Link1 và Link2 riêng biệt
- Dễ dàng copy kết quả

---

## 🛠️ Chức năng chính

### 📁 Quản lý thư mục

#### ➕ Tạo thư mục mới
1. Click nút **➕ Tạo** trong phần "Quản lý thư mục"
2. Nhập tên thư mục
3. Click OK

#### 🗑️ Xóa thư mục
1. Chọn thư mục cần xóa từ dropdown
2. Click nút **🗑️ Xóa**
3. Xác nhận xóa
- ⚠️ **Lưu ý**: Không thể xóa thư mục "default"

#### ✏️ Đổi tên thư mục
1. Chọn thư mục cần đổi tên
2. Click nút **✏️ Đổi tên**
3. Nhập tên mới
4. Click OK

#### 🔄 Làm mới danh sách
- Click nút **🔄 Làm mới** để cập nhật danh sách thư mục

#### 💾 Tải lại DB
- Click nút **💾 Tải DB** để tải lại dữ liệu từ file JSON

---

### 📝 Nhập dữ liệu

#### Nhập dữ liệu hàng loạt
1. Click chuột phải vào bảng → Chọn **📝 Nhập dữ liệu**
2. Cấu hình:
   - **Ánh xạ cột**: Chọn trường dữ liệu cho mỗi cột (TypeBM, ID, BmID, Link1)
   - **Dấu phân cách**: Ký tự phân cách giữa các trường (mặc định: `|`)
3. Nhập dữ liệu theo định dạng:
   ```
   TypeBM|ID|BmID|Link1|Link2|Link3
   Type1|123456|BM123|https://link1.com|https://link2.com|https://link3.com
   Type2|789012|BM456|https://link4.com||
   ```
4. Click **📥 Nhập hàng loạt**

#### Kết quả nhập
- ✅ **Thêm mới**: Số bản ghi được thêm vào
- ⚠️ **Trùng**: Số bản ghi trùng lặp (sẽ merge link vào bản ghi hiện có)
- ❌ **Lỗi**: Số dòng thiếu dữ liệu hoặc sai định dạng

---

### ✅ Chọn dữ liệu

#### Chọn tất cả
- Chuột phải → **✅ Chọn tất cả**
- Hoặc click vào checkbox ở cột "Chọn"

#### Chọn theo điều kiện
Chuột phải → **🎯 Chọn theo điều kiện**, sau đó chọn một trong các cách:

1. **📊 Chọn theo Type BM**
   - Nhập Type BM cần tìm
   - Click **✅ Chọn**

2. **🆔 Chọn theo ID**
   - Nhập danh sách ID (mỗi dòng một ID)
   - Click **✅ Chọn theo ID**

3. **🔢 Chọn theo BmID**
   - Nhập danh sách BmID (mỗi dòng một BmID)
   - Click **✅ Chọn theo BmID**

4. **🔗 Chọn theo Link**
   - Nhập danh sách Link (mỗi dòng một Link)
   - Click **✅ Chọn theo Link**

#### Bỏ chọn
- Chuột phải → **❌ Bỏ chọn tất cả**

---

### 📦 Di chuyển dữ liệu

#### Di chuyển sang thư mục khác
1. Chọn các dòng cần di chuyển
2. Click nút **📦 Move** trong phần "Quản lý thư mục"
3. Chọn thư mục đích
4. Chọn phạm vi di chuyển:
   - **📋 Toàn bộ**: Di chuyển tất cả links (Link1 + Link2 + Link3)
   - **🔗 Chỉ Link 1**: Chỉ di chuyển Link1
   - **🔗 Chỉ Link 2**: Chỉ di chuyển Link2
   - **🔗 Chỉ Link 3**: Chỉ di chuyển Link3
5. Click **✅ Xác nhận di chuyển**

#### Quy tắc di chuyển
- Nếu di chuyển **toàn bộ**: Bản ghi sẽ bị xóa khỏi thư mục nguồn
- Nếu di chuyển **một link**: Link được chọn sẽ bị xóa, các link còn lại được giữ nguyên
- Nếu thư mục đích đã có bản ghi trùng khóa (TypeBM + ID + BmID):
  - Link mới sẽ được merge vào các slot trống (Link1, Link2, Link3)
  - Không tạo bản ghi trùng lặp

---

### 📋 Copy dữ liệu

1. Chọn các dòng cần copy
2. Chuột phải → **📋 Copy dữ liệu**
3. Cấu hình:
   - **Ánh xạ cột**: Chọn 4 trường dữ liệu muốn copy
   - **Dấu phân cách**: Ký tự phân cách (mặc định: `|`)
4. Click **📋 Copy ngay**
5. Dữ liệu được copy vào clipboard, có thể paste vào Excel, Notepad, v.v.

**Ví dụ output**:
```
TypeBM|ID|BmID|Link1
Type1|123456|BM123|https://link1.com
Type2|789012|BM456|https://link2.com
```

---

### 📝 Thêm ghi chú

1. Chọn các dòng cần thêm ghi chú
2. Chuột phải → **📝 Thêm ghi chú**
3. Nhập nội dung ghi chú
4. Click OK
- Ghi chú sẽ được áp dụng cho tất cả dòng đã chọn

---

### 🗑️ Xóa dữ liệu

1. Chọn các dòng cần xóa
2. Chuột phải → **🗑️ Xóa đã chọn**
3. Xác nhận xóa
- ⚠️ **Lưu ý**: Hành động này không thể hoàn tác

---

### 🔍 Lọc Link theo BmID

1. Chuyển sang tab **🔍 Lọc Link**
2. Nhập danh sách BmID (mỗi dòng một BmID) vào ô text
3. Click **🔍 Lọc ngay**
4. Kết quả hiển thị:
   - **🔗 Link 1**: Tất cả Link1 khớp với BmID
   - **🔗 Link 2**: Tất cả Link2 khớp với BmID
5. Copy link từ danh sách để sử dụng

---

### ✏️ Sửa dữ liệu trực tiếp

#### Sửa một ô
1. **Double-click** vào ô cần sửa
2. Nhập giá trị mới
3. Nhấn **Enter** để lưu hoặc **Esc** để hủy

#### Các cột có thể sửa
- ✅ TypeBM, ID, BmID
- ✅ Link1, Link2, Link3
- ✅ Ghi chú
- ❌ STT, Chọn, Thư mục (không sửa được)

---

### 📊 Sắp xếp dữ liệu

- Click vào **tiêu đề cột** để sắp xếp
- Click lần 1: Sắp xếp tăng dần (A→Z)
- Click lần 2: Sắp xếp giảm dần (Z→A)
- Áp dụng cho: TypeBM, ID, BmID, Link1, Link2, Link3, Ghi chú

---

## ⌨️ Các phím tắt

| Phím tắt | Chức năng |
|----------|-----------|
| **Ctrl + C** | Copy nội dung ô đang chọn |
| **Double Click** | Sửa ô |
| **Enter** | Lưu sau khi sửa |
| **Esc** | Hủy sửa |
| **Click chuột phải** | Mở menu context |
| **Click checkbox** | Toggle chọn/bỏ chọn dòng |

---

## 📂 Import/Export

### 📥 Import CSV
1. Chuột phải → **Import CSV** (nếu có)
2. Chọn file CSV
3. Chọn chế độ:
   - **Thêm vào**: Thêm vào dữ liệu hiện tại
   - **Thay thế**: Xóa dữ liệu cũ và import mới

### 📤 Export CSV
1. Chuột phải → **Export CSV** (nếu có)
2. Chọn vị trí lưu file
3. File CSV sẽ chứa đầy đủ thông tin: TypeBM, ID, BmID, Link1, Link2, Link3, Note

---

## 💾 Lưu trữ dữ liệu

### Tự động lưu
- Dữ liệu được lưu tự động sau mỗi thao tác:
  - Nhập dữ liệu hàng loạt
  - Sửa ô
  - Xóa dòng
  - Thêm ghi chú
  - Di chuyển dữ liệu

### File JSON
- Mỗi thư mục có file `bm_data.json` riêng
- Đường dẫn: `bm_data/{tên_thư_mục}/bm_data.json`
- Định dạng JSON chuẩn, dễ đọc và chỉnh sửa thủ công nếu cần

### Cấu trúc dữ liệu
```json
[
  {
    "TypeBM": "Type1",
    "ID": "123456",
    "BmID": "BM123",
    "Link1": "https://link1.com",
    "Link2": "https://link2.com",
    "Link3": "https://link3.com",
    "Note": "Ghi chú mẫu"
  }
]
```

---

## ⚠️ Lưu ý quan trọng

### Khóa chính
- Mỗi bản ghi được định danh duy nhất bởi: **(TypeBM + ID + BmID)**
- Khi import/nhập dữ liệu trùng khóa:
  - Link mới sẽ được merge vào slot trống
  - Không tạo bản ghi mới

### Di chuyển dữ liệu
- **Toàn bộ**: Xóa bản ghi khỏi thư mục nguồn
- **Một link**: Chỉ xóa link đó, giữ lại bản ghi nếu còn link khác
- Nếu tất cả link bị xóa → Bản ghi bị xóa hoàn toàn

### Thư mục default
- Không thể xóa hoặc đổi tên thư mục "default"
- Thư mục "default" luôn tồn tại

### Hiệu suất
- Ứng dụng được tối ưu cho việc xử lý hàng loạt
- Có thể xử lý hàng nghìn bản ghi mà không bị lag
- Sử dụng cursor "wait" khi đang xử lý để báo hiệu

### Backup
- Nên backup thư mục `bm_data/` định kỳ
- File JSON có thể copy trực tiếp để backup

---

## 🎨 Giao diện hiện đại

### Màu sắc
- **Primary (Blue)**: Nút chính, header bảng
- **Success (Green)**: Nút tạo, xác nhận
- **Danger (Red)**: Nút xóa, hủy
- **Accent (Amber)**: Nút phụ

### Responsive
- Giao diện tự động căn chỉnh theo kích thước màn hình
- Maximize tự động khi khởi động
- Scrollbar xuất hiện khi cần thiết

### Icons
- Sử dụng emoji để làm icon trực quan
- Dễ nhận biết chức năng qua icon

---

## 🆘 Xử lý sự cố

### Lỗi không load được dữ liệu
- Kiểm tra file `bm_data/{thư_mục}/bm_data.json` có tồn tại không
- Kiểm tra định dạng JSON có hợp lệ không
- Thử click **💾 Tải DB** để reload

### Lỗi không lưu được
- Kiểm tra quyền ghi vào thư mục
- Đảm bảo không bị lock file bởi ứng dụng khác

### Dữ liệu không cập nhật
- Click **🔄 Làm mới** trong phần quản lý thư mục
- Restart ứng dụng

### Checkbox không đồng bộ
- Ứng dụng tự động đồng bộ sau mỗi thao tác
- Nếu vẫn lỗi, thử bỏ chọn tất cả rồi chọn lại

---

## 📞 Hỗ trợ

Nếu gặp vấn đề hoặc có đề xuất cải tiến, vui lòng:
- Kiểm tra lại hướng dẫn sử dụng
- Xem phần Xử lý sự cố
- Liên hệ với đội ngũ phát triển

---

## 📝 Changelog

### Version 1.0
- ✅ Quản lý thư mục (tạo, xóa, đổi tên)
- ✅ Nhập dữ liệu hàng loạt
- ✅ Chọn theo nhiều điều kiện
- ✅ Di chuyển dữ liệu giữa thư mục
- ✅ Copy dữ liệu với cấu hình linh hoạt
- ✅ Sửa trực tiếp trên bảng
- ✅ Lọc link theo BmID
- ✅ Giao diện hiện đại, dễ sử dụng
- ✅ Hỗ trợ 3 link cho mỗi BM
- ✅ Tối ưu hiệu suất

---

**🎉 Chúc bạn sử dụng BM Manager Pro hiệu quả!**