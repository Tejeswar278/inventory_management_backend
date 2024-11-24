from flask import Blueprint, request
from ..controllers import controller_admin

admin_routes = Blueprint('admin_routes',__name__)

@admin_routes.route('/create_category',methods=['POST'])
def create_category():
    data = request.json
    result = controller_admin.create_category_cont(data)
    return result

@admin_routes.route('/add_products',methods=['POST'])
def add_products():
    data = request.json
    result = controller_admin.add_products_cont(data)
    return result

@admin_routes.route('/edit_product',methods=['POST'])
def edit_product():
    data = request.json
    result = controller_admin.edit_product_cont(data)
    return result

@admin_routes.route('/delete_category',methods=['POST'])
def delete_category():
    data = request.json
    result = controller_admin.delete_category_cont(data)
    return result

@admin_routes.route('/delete_product',methods=['POST'])
def delete_product():
    data = request.json
    result = controller_admin.delete_product_cont(data)
    return result