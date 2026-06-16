# Bảng Test Case - Hệ thống quản lý đơn hàng đơn giản

## 1. Chức năng tạo đơn hàng

| TC | Dữ liệu kiểm thử | Kết quả mong đợi | Loại kiểm thử |
|---|---|---|---|
| TC01 | Mã đơn hàng DH001, sản phẩm Áo thun, số lượng 2, đơn giá 100000 | Tạo đơn hàng thành công | Hộp đen |
| TC02 | Tên sản phẩm rỗng | Hiển thị lỗi tên sản phẩm không được để trống | Hộp đen |
| TC03 | Số lượng bằng 0 | Hiển thị lỗi số lượng phải lớn hơn 0 | Hộp đen |
| TC04 | Đơn giá âm | Hiển thị lỗi đơn giá phải lớn hơn 0 | Hộp đen |

## 2. Chức năng tính tổng tiền

| TC | Dữ liệu kiểm thử | Kết quả mong đợi | Loại kiểm thử |
|---|---|---|---|
| TC05 | 2 sản phẩm, đơn giá 100000 | Tổng tiền là 200000 | Hộp đen |
| TC06 | 3 sản phẩm, đơn giá 20000 | Tổng tiền là 60000 | Hộp trắng |

## 3. Chức năng áp dụng giảm giá

| TC | Dữ liệu kiểm thử | Kết quả mong đợi | Loại kiểm thử |
|---|---|---|---|
| TC07 | Tổng tiền 100000, giảm giá 10% | Tổng sau giảm là 90000 | Hộp đen |
| TC08 | Giảm giá 0% | Tổng tiền không thay đổi | Hộp đen |
| TC09 | Giảm giá 100% | Tổng tiền còn 0 | Hộp trắng |
| TC10 | Giảm giá -1% | Hiển thị lỗi giảm giá không hợp lệ | Hộp trắng |
| TC11 | Giảm giá 120% | Hiển thị lỗi giảm giá không hợp lệ | Hộp đen |

## 4. Chức năng kiểm tra và cập nhật trạng thái

| TC | Dữ liệu kiểm thử | Kết quả mong đợi | Loại kiểm thử |
|---|---|---|---|
| TC12 | Chờ xử lý → Đang xử lý | Cập nhật thành công | Hộp trắng |
| TC13 | Chờ xử lý → Hoàn thành | Báo lỗi chuyển trạng thái không hợp lệ | Hộp trắng |
| TC14 | Đang giao → Hoàn thành | Cập nhật thành công | Hộp trắng |
| TC15 | Hoàn thành → Đã hủy | Báo lỗi chuyển trạng thái không hợp lệ | Hộp trắng |
