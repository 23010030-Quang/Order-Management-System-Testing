class ValidationError(Exception):
    """Lỗi dữ liệu đầu vào không hợp lệ."""


class InvalidStatusTransitionError(Exception):
    """Lỗi khi chuyển trạng thái đơn hàng không hợp lệ."""
