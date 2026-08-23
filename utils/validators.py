def validate_product(name, category, price, quantity):
    if name is None or not str(name).strip():
        raise ValueError("Product name cannot be empty.")

    if category is None or not str(category).strip():
        raise ValueError("Category cannot be empty.")

    try:
        price = float(price)
        quantity = int(quantity)
    except (TypeError, ValueError):
        raise ValueError("Price and quantity must be numeric values.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    return True