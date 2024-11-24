from flask import Blueprint, request
from ..controllers import controller_orders

orders_routes = Blueprint('orders_routes',__name__)

@orders_routes.route('/create_order',methods=['POST'])
def create_order():
    data = request.json
    result = controller_orders.create_order_cont(data)
    return result

@orders_routes.route('/get_orders',methods=['GET'])
def get_orders():
    result = controller_orders.get_orders()
    return result