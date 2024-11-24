from flask import jsonify
from ..databases.mongodb import CategoriesProducts

def get_categories():
    try:
        # Fetch all categories from the database
        categories = CategoriesProducts.objects()

        # Prepare the list of categories
        categories_list = [
            {
                "category_id": str(category.id),
                "category_name": category.name,
                "products": [
                    {
                        "product_name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                        "description": product.description,
                    }
                    for product in category.products
                ],
                "total_products": len(category.products),
            }
            for category in categories
        ]

        # Prepare the response
        response = {
            "message": "Categories fetched successfully",
            "categories": categories_list,
            "total_categories": len(categories_list),
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching categories", "error": str(e)}), 500

def get_categories_list():
    try:
        # Fetch all categories from the database
        categories = CategoriesProducts.objects.only('id', 'name')

        # Prepare a list of category names and IDs
        categories_list = [
            {
                "category_id": str(category.id),
                "category_name": category.name,
            }
            for category in categories
        ]

        # Prepare the response
        response = {
            "message": "Category names fetched successfully",
            "categories": categories_list,
            "total_categories": len(categories_list),
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching category names", "error": str(e)}), 500

def get_category_by_name(data):
    try:
        category_name = data.get('category_name')

        if not category_name:
            return jsonify({"message": "Category name is required"}), 400

        category = CategoriesProducts.objects(name=category_name).first()

        if not category:
            return jsonify({"message": f"Category '{category_name}' does not exist"}), 404

        products = [
            {
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "description": product.description,
            }
            for product in category.products
        ]

        response = {
            "message": f"Category '{category_name}' fetched successfully",
            "category_id": str(category.id),
            "category_name": category.name,
            "products": products,
            "total_products": len(products),
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching the category", "error": str(e)}), 500

