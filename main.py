from order_system.models import OrderStatus, create_order


if __name__ == "__main__":
    order = create_order(
        order_id="DH001",
        products=[
            ("Áo thun", 2, 100000),
            ("Quần jeans", 1, 250000),
        ],
        discount_percent=10,
    )

    print("Thông tin đơn hàng ban đầu:")
    print(order.as_dict())

    order.update_status(OrderStatus.PROCESSING)
    order.update_status(OrderStatus.SHIPPING)

    print("\nSau khi cập nhật trạng thái:")
    print(order.as_dict())
