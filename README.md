# Order Management Testing

Dự án mẫu phục vụ bài báo cáo **Kiểm thử và đánh giá chất lượng hệ thống quản lý đơn hàng đơn giản**.

## 1. Mục tiêu

Hệ thống cho phép:

- Tạo đơn hàng
- Tính tổng tiền
- Áp dụng giảm giá
- Kiểm tra và cập nhật trạng thái đơn hàng
- Thực hiện kiểm thử hộp đen và hộp trắng bằng `pytest`

## 2. Cấu trúc thư mục

```text
order-management-testing/
├── order_system/
│   ├── __init__.py
│   ├── exceptions.py
│   └── models.py
├── tests/
│   ├── test_order_blackbox.py
│   └── test_order_whitebox.py
├── docs/
│   └── test_cases.md
├── main.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## 3. Cài đặt môi trường

Tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
```

## 4. Chạy chương trình mẫu

```bash
python main.py
```

## 5. Chạy kiểm thử

Chạy toàn bộ test case:

```bash
pytest
```

Chạy kiểm thử kèm báo cáo độ bao phủ code:

```bash
pytest --cov=order_system
```

## 6. Nội dung kiểm thử

### Kiểm thử hộp đen

Tập trung vào đầu vào và đầu ra của hệ thống:

- Tạo đơn hàng hợp lệ
- Tạo đơn hàng với dữ liệu thiếu hoặc sai
- Tính tổng tiền
- Áp dụng giảm giá hợp lệ và không hợp lệ
- Kiểm tra trạng thái đơn hàng

### Kiểm thử hộp trắng

Tập trung vào logic xử lý bên trong:

- Kiểm tra các nhánh xử lý dữ liệu đầu vào
- Kiểm tra điều kiện giảm giá
- Kiểm tra quy tắc chuyển trạng thái đơn hàng
- Kiểm tra các ngoại lệ trong hệ thống

## 7. Quy tắc trạng thái đơn hàng

| Trạng thái hiện tại | Trạng thái tiếp theo hợp lệ |
|---|---|
| Chờ xử lý | Đang xử lý, Đã hủy |
| Đang xử lý | Đang giao, Đã hủy |
| Đang giao | Hoàn thành |
| Hoàn thành | Không được chuyển tiếp |
| Đã hủy | Không được chuyển tiếp |
