from flask import Blueprint, request
from ..controllers import controller_dashboard

dashboard_routes = Blueprint('dashboard_routes',__name__)

@dashboard_routes.route('/get_products',methods=['GET'])
def get_products():
    result = controller_dashboard.get_categories()
    return result

@dashboard_routes.route('/get_category_list',methods=['GET'])
def get_category_list():
    result = controller_dashboard.get_categories_list()
    return result

@dashboard_routes.route('/get_category',methods=['POST'])
def get_category_products():
    data = request.json
    result = controller_dashboard.get_category_by_name(data)
    return result