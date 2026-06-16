from decimal import Decimal

import pytest

from order_system.exceptions import ValidationError
from order_system.models import OrderStatus, create_order


# Kiểm thử hộp đen: tập trung vào đầu vào và đầu ra, không xét code bên trong.


def test_create_order_with_valid_data_should_success():
    order = create_order(
        order_id="DH001",
        products=[("Áo thun", 2, 100000), ("Mũ", 1, 50000)],
    )

    assert order.order_id == "DH001"
    assert order.subtotal == Decimal("250000.00")
    assert order.total == Decimal("250000.00")
    assert order.status == OrderStatus.PENDING


def test_calculate_total_with_10_percent_discount():
    order = create_order(
        order_id="DH002",
        products=[("Giày", 2, 500000)],
        discount_percent=10,
    )

    assert order.subtotal == Decimal("1000000.00")
    assert order.discount_amount == Decimal("100000.00")
    assert order.total == Decimal("900000.00")


def test_calculate_total_with_0_percent_discount():
    order = create_order(
        order_id="DH003",
        products=[("Balo", 1, 300000)],
        discount_percent=0,
    )

    assert order.total == Decimal("300000.00")


def test_create_order_with_empty_product_name_should_fail():
    with pytest.raises(ValidationError, match="Tên sản phẩm không được để trống"):
        create_order(order_id="DH004", products=[("", 1, 100000)])


def test_create_order_with_zero_quantity_should_fail():
    with pytest.raises(ValidationError, match="Số lượng phải lớn hơn 0"):
        create_order(order_id="DH005", products=[("Áo thun", 0, 100000)])


def test_create_order_with_negative_price_should_fail():
    with pytest.raises(ValidationError, match="Đơn giá phải lớn hơn 0"):
        create_order(order_id="DH006", products=[("Áo thun", 1, -100000)])


def test_create_order_with_invalid_discount_should_fail():
    with pytest.raises(ValidationError, match="Giảm giá phải nằm trong khoảng"):
        create_order(order_id="DH007", products=[("Áo thun", 1, 100000)], discount_percent=120)


def test_check_order_status_after_update():
    order = create_order(order_id="DH008", products=[("Áo thun", 1, 100000)])

    result = order.update_status("PROCESSING")

    assert result == OrderStatus.PROCESSING
    assert order.status.value == "Đang xử lý"
