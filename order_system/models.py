from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Iterable, Union

from .exceptions import InvalidStatusTransitionError, ValidationError

MoneyInput = Union[int, float, str, Decimal]


def to_decimal(value: MoneyInput) -> Decimal:
    """Chuyển dữ liệu tiền tệ về Decimal và làm tròn 2 chữ số thập phân."""
    try:
        decimal_value = Decimal(str(value))
    except Exception as exc:
        raise ValidationError("Giá trị tiền tệ không hợp lệ") from exc

    return decimal_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class OrderStatus(str, Enum):
    """Các trạng thái hợp lệ của đơn hàng."""

    PENDING = "Chờ xử lý"
    PROCESSING = "Đang xử lý"
    SHIPPING = "Đang giao"
    COMPLETED = "Hoàn thành"
    CANCELLED = "Đã hủy"


@dataclass
class OrderItem:
    """Sản phẩm trong đơn hàng."""

    product_name: str
    quantity: int
    unit_price: MoneyInput

    def __post_init__(self) -> None:
        if not self.product_name or not self.product_name.strip():
            raise ValidationError("Tên sản phẩm không được để trống")

        if not isinstance(self.quantity, int):
            raise ValidationError("Số lượng phải là số nguyên")

        if self.quantity <= 0:
            raise ValidationError("Số lượng phải lớn hơn 0")

        self.unit_price = to_decimal(self.unit_price)

        if self.unit_price <= 0:
            raise ValidationError("Đơn giá phải lớn hơn 0")

    @property
    def total_price(self) -> Decimal:
        """Tính tiền của một dòng sản phẩm."""
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"))


@dataclass
class Order:
    """Đơn hàng đơn giản gồm sản phẩm, giảm giá và trạng thái."""

    order_id: str
    items: list[OrderItem] = field(default_factory=list)
    discount_percent: MoneyInput = Decimal("0")
    status: OrderStatus = OrderStatus.PENDING

    # Quy tắc chuyển trạng thái đơn hàng
    ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING: {OrderStatus.PROCESSING, OrderStatus.CANCELLED},
        OrderStatus.PROCESSING: {OrderStatus.SHIPPING, OrderStatus.CANCELLED},
        OrderStatus.SHIPPING: {OrderStatus.COMPLETED},
        OrderStatus.COMPLETED: set(),
        OrderStatus.CANCELLED: set(),
    }

    def __post_init__(self) -> None:
        if not self.order_id or not self.order_id.strip():
            raise ValidationError("Mã đơn hàng không được để trống")

        if not self.items:
            raise ValidationError("Đơn hàng phải có ít nhất một sản phẩm")

        self.discount_percent = to_decimal(self.discount_percent)

        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValidationError("Giảm giá phải nằm trong khoảng từ 0 đến 100%")

        if isinstance(self.status, str):
            self.status = self._parse_status(self.status)

    @staticmethod
    def _parse_status(status: str) -> OrderStatus:
        for valid_status in OrderStatus:
            if status == valid_status.value or status == valid_status.name:
                return valid_status
        raise ValidationError("Trạng thái đơn hàng không hợp lệ")

    @property
    def subtotal(self) -> Decimal:
        """Tổng tiền trước giảm giá."""
        return sum((item.total_price for item in self.items), Decimal("0.00")).quantize(
            Decimal("0.01")
        )

    @property
    def discount_amount(self) -> Decimal:
        """Số tiền được giảm."""
        return (self.subtotal * self.discount_percent / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def total(self) -> Decimal:
        """Tổng tiền sau khi áp dụng giảm giá."""
        return (self.subtotal - self.discount_amount).quantize(Decimal("0.01"))

    def add_item(self, item: OrderItem) -> None:
        """Thêm sản phẩm vào đơn hàng."""
        if not isinstance(item, OrderItem):
            raise ValidationError("Sản phẩm thêm vào đơn hàng không hợp lệ")
        self.items.append(item)

    def update_status(self, new_status: Union[str, OrderStatus]) -> OrderStatus:
        """Cập nhật trạng thái đơn hàng theo đúng quy trình xử lý."""
        if isinstance(new_status, str):
            new_status = self._parse_status(new_status)

        allowed_next_statuses = self.ALLOWED_TRANSITIONS[self.status]
        if new_status not in allowed_next_statuses:
            raise InvalidStatusTransitionError(
                f"Không thể chuyển trạng thái từ '{self.status.value}' sang '{new_status.value}'"
            )

        self.status = new_status
        return self.status

    def as_dict(self) -> dict:
        """Trả về thông tin đơn hàng ở dạng dict để dễ hiển thị hoặc kiểm thử."""
        return {
            "order_id": self.order_id,
            "items": [
                {
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "total_price": str(item.total_price),
                }
                for item in self.items
            ],
            "subtotal": str(self.subtotal),
            "discount_percent": str(self.discount_percent),
            "discount_amount": str(self.discount_amount),
            "total": str(self.total),
            "status": self.status.value,
        }


def create_order(
    order_id: str,
    products: Iterable[tuple[str, int, MoneyInput]],
    discount_percent: MoneyInput = 0,
) -> Order:
    """Hàm tiện ích để tạo đơn hàng từ danh sách tuple."""
    items = [OrderItem(name, quantity, unit_price) for name, quantity, unit_price in products]
    return Order(order_id=order_id, items=items, discount_percent=discount_percent)
