def cart_context(request):
    cart = request.session.get("cart", {})
    total_items = sum(item["quantity"] for item in cart.values())
    total_price = sum(item["quantity"] * item["price"] for item in cart.values())
    return {
        "total_items": total_items,
        "total_price": total_price,
    }
