from flask import jsonify
from ..databases.mongodb import CategoriesProducts, Products

def create_category_cont(data):
    category_name = data.get('category')

    if not category_name:
        return jsonify({"message": "Category name is required"}), 400

    existing_category = CategoriesProducts.objects(name=category_name).first()

    if existing_category:
        return jsonify({"message": "Category already exists", "category": existing_category.to_json()}), 200

    new_category = CategoriesProducts(name=category_name)
    new_category.save()

    return jsonify({"message": "Category created successfully", "category": {"name": new_category.name}}), 201

def add_products_cont(data):
    category_name = data.get('category')
    products = data.get('products')

    if not category_name:
        return jsonify({"message": "Category name is required"}), 400
    
    if not products or not isinstance(products, list):
        return jsonify({"message": "Products must be a list"}), 400

    existing_category = CategoriesProducts.objects(name=category_name).first()

    if not existing_category:
        return jsonify({"message": f"Category '{category_name}' does not exist"}), 404

    already_existing_products = []
    new_products = []
    unique_input_products = set()  

    for product_data in products:
        product_name = product_data.get('name')

        if not product_name:
            continue  

        if product_name in unique_input_products:
            already_existing_products.append(product_name)
            continue

        unique_input_products.add(product_name)

        existing_product = next((p for p in existing_category.products if p.name == product_name), None)
        
        if existing_product:
            already_existing_products.append(product_name)
        else:
            new_products.append(Products(**product_data))

    if new_products:
        existing_category.products.extend(new_products)
        existing_category.save()

    response = {
        "message": "Products processed successfully",
        "already_existing_products": already_existing_products,
        "newly_added_products": [p.name for p in new_products],
    }

    return jsonify(response), 201

def edit_product_cont(data):
    category_name = data.get('category')
    product_name = data.get('product_name')
    product_updated_details = data.get('product_updated_details')

    if not category_name:
        return jsonify({"message": "Category name is required"}), 400

    if not product_name:
        return jsonify({"message": "Product name is required"}), 400

    if not product_updated_details or not isinstance(product_updated_details, dict):
        return jsonify({"message": "Product updated details must be a valid object"}), 400

    existing_category = CategoriesProducts.objects(name=category_name).first()

    if not existing_category:
        return jsonify({"message": f"Category '{category_name}' does not exist"}), 404

    product_to_edit = next((p for p in existing_category.products if p.name == product_name), None)

    if not product_to_edit:
        return jsonify({"message": f"Product '{product_name}' does not exist in category '{category_name}'"}), 404

    if 'name' in product_updated_details:
        product_to_edit.name = product_updated_details['name']
    if 'price' in product_updated_details:
        product_to_edit.price = product_updated_details['price']
    if 'quantity' in product_updated_details:
        product_to_edit.quantity = product_updated_details['quantity']
    if 'description' in product_updated_details:
        product_to_edit.description = product_updated_details['description']

    existing_category.save()

    response = {
        "message": "Product updated successfully",
        "updated_product": {
            "name": product_to_edit.name,
            "price": product_to_edit.price,
            "quantity": product_to_edit.quantity,
            "description": product_to_edit.description,
        },
    }

    return jsonify(response), 200
