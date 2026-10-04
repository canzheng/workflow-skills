def total(lines, shipping_cents=0):
    if not lines or any(type(price) is not int or type(quantity) is not int or price < 0 or quantity <= 0 for price, quantity in lines):
        raise ValueError('Invalid line items')
    if type(shipping_cents) is not int or shipping_cents < 0:
        raise ValueError('Invalid shipping_cents')
    return sum(price * quantity for price, quantity in lines) + shipping_cents
