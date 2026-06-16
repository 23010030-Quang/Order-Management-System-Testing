from decimal import Decimal

import pytest

from order_system.exceptions import InvalidStatusTransitionError, ValidationError
from order_system.models import Order, OrderItem, OrderStatus, to_decimal


# Kiểm thử hộp trắng: tập trung vào các nhánh xử lý và logic nội bộ.


def test_to_decimal_should_round_to_2_decimal_places():
    assert to_decimal("1000.555") == Decimal("1000.56")


def test_order_item_total_price_branch():
    item = OrderItem(product_name="Sách", quantity=3, unit_price=20000)

    assert item.total_price == Decimal("60000.00")


def test_order_requires_at_least_one_item_branch():
    with pytest.raises(ValidationError, match="Đơn hàng phải có ít nhất một sản phẩm"):
        Order(order_id="DH009", items=[])


def test_discount_lower_than_0_branch():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)

    with pytest.raises(ValidationError, match="Giảm giá phải nằm trong khoảng"):
        Order(order_id="DH010", items=[item], discount_percent=-1)


def test_discount_equal_100_should_make_total_zero():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)
    order = Order(order_id="DH011", items=[item], discount_percent=100)

    assert order.discount_amount == Decimal("100000.00")
    assert order.total == Decimal("0.00")


def test_parse_valid_vietnamese_status():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)
    order = Order(order_id="DH012", items=[item], status="Chờ xử lý")

    assert order.status == OrderStatus.PENDING


def test_parse_invalid_status_branch():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)

    with pytest.raises(ValidationError, match="Trạng thái đơn hàng không hợp lệ"):
        Order(order_id="DH013", items=[item], status="Không xác định")


def test_valid_status_transition_from_pending_to_processing():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)
    order = Order(order_id="DH014", items=[item])

    order.update_status(OrderStatus.PROCESSING)

    assert order.status == OrderStatus.PROCESSING


def test_invalid_status_transition_from_pending_to_completed():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)
    order = Order(order_id="DH015", items=[item])

    with pytest.raises(InvalidStatusTransitionError, match="Không thể chuyển trạng thái"):
        order.update_status(OrderStatus.COMPLETED)


def test_completed_order_cannot_change_status():
    item = OrderItem(product_name="Sách", quantity=1, unit_price=100000)
    order = Order(order_id="DH016", items=[item], status=OrderStatus.SHIPPING)
    order.update_status(OrderStatus.COMPLETED)

    with pytest.raises(InvalidStatusTransitionError, match="Không thể chuyển trạng thái"):
        order.update_status(OrderStatus.CANCELLED)
