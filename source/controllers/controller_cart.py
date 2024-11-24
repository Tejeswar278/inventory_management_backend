from flask import jsonify
from ..databases.mongodb import Cart, CategoriesProducts

def add_to_cart_cont(data):
    products = data.get('products')
    if not isinstance(products, list) or not products:
        return jsonify({"message": "Input must be a non-empty array of products"}), 400

    already_existing_products = []
    newly_added_products = []

    for product in products:
        product_name = product.get('name')
        category_name = product.get('category_name')
        quantity = product.get('quantity', 1)
        price = product.get('price')

        if not product_name or not category_name:
            return jsonify({"message": "Each product must have a product_name and category_name"}), 400

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"message": f"Invalid quantity for product '{product_name}'"}), 400

        if not price or not isinstance(price, int) or price <= 0:
            return jsonify({"message": f"Invalid price for product '{product_name}'"}), 400

        # Find the category
        category = CategoriesProducts.objects(name=category_name).first()
        if not category:
            return jsonify({"message": f"Category '{category_name}' not found"}), 404

        # Find the product in the category
        product_in_category = next((p for p in category.products if p.name == product_name), None)
        if not product_in_category:
            return jsonify({"message": f"Product '{product_name}' not found in category '{category_name}'"}), 404

        if product_in_category.quantity < quantity:
            return jsonify({"message": f"Insufficient quantity for product '{product_name}' in category '{category_name}'"}), 400

        # Decrease the quantity in the category's product
        product_in_category.quantity -= quantity
        category.save()

        # Add to Cart collection
        existing_product = Cart.objects(product_name=product_name).first()

        if existing_product:
            existing_product.quantity += quantity
            existing_product.save()
            already_existing_products.append({
                "product_name": product_name,
                "updated_quantity": existing_product.quantity,
                "category_name":category_name
            })
        else:
            new_product = Cart(product_name=product_name, quantity=quantity, price=price,category_name=category_name )
            new_product.save()
            newly_added_products.append({
                "product_name": product_name,
                "quantity": quantity,
                "category_name":category_name
            })

    response = {
        "message": "Products processed successfully",
        "already_existing_products": already_existing_products,
        "newly_added_products": newly_added_products,
    }

    return jsonify(response), 200



def get_cart_items():
    try:

        products_list = []
        cart_products = Cart.objects()

        response = {
            "message": "Cart products fetched successfully",
            "products": products_list,
            "total_items": 0,
            "total_cart_value": 0
        }

        # Format the products into a list of dictionaries
        if cart_products:
            products_list = [
                {
                    "product_name": product.product_name,
                    "quantity": product.quantity,
                    "price": product.price,
                    "category_name":product.category_name,
                    "total_price": product.quantity * product.price
                }
                for product in cart_products
            ]

            response = {
                "message": "Cart products fetched successfully",
                "products": products_list,
                "total_items": len(products_list),
                "total_cart_value": sum(product["total_price"] for product in products_list)
            }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching cart products", "error": str(e)}), 500

def remove_item_cont(data):
    product_name = data.get('product_name')
    quantity = data.get('quantity')
    category_name = data.get('category_name')

    # Validate the input
    if not product_name or not category_name:
        return jsonify({"message": "Each product must have a product_name and category_name"}), 400

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "Invalid quantity to remove"}), 400

    # Find the product in the Cart collection
    cart_product = Cart.objects(product_name=product_name).first()
    if not cart_product:
        return jsonify({"message": f"Product '{product_name}' not found in the cart"}), 404

    # Check if the cart has enough quantity of the product
    if cart_product.quantity < quantity:
        return jsonify({"message": f"Insufficient quantity in cart for product '{product_name}'"}), 400

    # Find the category and product in CategoriesProducts collection
    category = CategoriesProducts.objects(name=category_name).first()
    if not category:
        return jsonify({"message": f"Category '{category_name}' not found"}), 404

    product_in_category = next((p for p in category.products if p.name == product_name), None)
    if not product_in_category:
        return jsonify({"message": f"Product '{product_name}' not found in category '{category_name}'"}), 404

    # Increase the quantity in CategoriesProducts collection
    product_in_category.quantity += quantity
    category.save()

    # Remove the product from the Cart collection
    cart_product.quantity -= quantity

    # If quantity is now zero, delete the product from the cart
    if cart_product.quantity == 0:
        cart_product.delete()
    else:
        cart_product.save()

    return jsonify({"message": f"Successfully removed {quantity} of '{product_name}' from the cart"}), 200
