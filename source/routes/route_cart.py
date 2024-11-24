from flask import Blueprint, request
from ..controllers import controller_cart

cart_routes = Blueprint('cart_routes',__name__)

@cart_routes.route('/add_to_cart',methods=['POST'])
def add_to_cart():
    data = request.json
    result = controller_cart.add_to_cart_cont(data)
    return result

@cart_routes.route('/get_cart',methods=['GET'])
def get_cart():
    result = controller_cart.get_cart_items()
    return result

@cart_routes.route('/remove_item',methods=['POST'])
def remove_item():
    data = request.json
    result = controller_cart.remove_item_cont(data)
    return result