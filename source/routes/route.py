from flask import Blueprint, request
from ..controllers import controller

routes = Blueprint('routes',__name__)

@routes.route('/create_category',methods=['POST'])
def create_category():
    data = request.json
    result = controller.create_category_cont(data)
    return result

@routes.route('/add_products',methods=['POST'])
def add_products():
    data = request.json
    result = controller.add_products_cont(data)
    return result

@routes.route('/edit_product',methods=['POST'])
def edit_product():
    data = request.json
    result = controller.edit_product_cont(data)
    return result