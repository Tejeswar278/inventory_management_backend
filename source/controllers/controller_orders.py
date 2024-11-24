import uuid
from flask import jsonify
from datetime import datetime
from ..databases.mongodb import Orders, Cart

def create_order_cont(data):
    try:
        products = data.get('products')
        total_items = data.get('total_items')
        total_cart_value = data.get('total_cart_value')

        if not products or not isinstance(products, list):
            return jsonify({"message": "Products are required and must be a list"}), 400
        
        if total_items is None or total_cart_value is None:
            return jsonify({"message": "Total items and total cart value are required"}), 400

        order_id = str(uuid.uuid4())
        order_date = datetime.utcnow()

        # Create the order
        order = Orders(
            order_id=order_id,
            order_date=order_date,
            products=products,
            total_items=total_items,
            total_cart_value=total_cart_value
        )

        # Save the order to the database
        order.save()

        # Clear the Cart collection
        Cart.objects.delete()

        # Prepare the response
        response = {
            "message": "Order created successfully",
            "order_id": order_id,
            "order_date": order_date.isoformat(),
            "total_items": total_items,
            "total_cart_value": total_cart_value
        }

        return jsonify(response), 201

    except Exception as e:
        return jsonify({"message": "An error occurred while creating the order", "error": str(e)}), 500


def get_orders():
    try:
        orders_list = []
        total_orders_value = 0

        orders = Orders.objects()

        for order in orders:
            order_details = {
                "order_id": order.order_id,
                "order_date": order.order_date.isoformat(),
                "products": order.products,
                "total_items": order.total_items
            }
            orders_list.append(order_details)
            total_orders_value += order.total_cart_value

        # Prepare response
        response = {
            "message": "Orders fetched successfully",
            "orders": orders_list,
            "total_orders": len(orders_list),
            "total_orders_value": total_orders_value,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching orders", "error": str(e)}), 500