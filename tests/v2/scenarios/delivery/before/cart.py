def total(lines):
    if not lines or any(price < 0 or quantity <= 0 for price, quantity in lines):
        raise ValueError('Invalid line items')
    return sum(price for price, quantity in lines)  # defect: ignores quantity
