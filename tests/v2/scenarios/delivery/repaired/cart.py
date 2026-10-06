def total(lines):
    if not lines or any(type(price) is not int or type(quantity) is not int or price < 0 or quantity <= 0 for price, quantity in lines):
        raise ValueError('Invalid line items')
    return sum(price * quantity for price, quantity in lines)
