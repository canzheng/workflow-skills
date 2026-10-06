"""Current fixture implementation inspected during the shaping exercise."""
def single_item_cents(price_cents):
    if type(price_cents) is not int or price_cents < 0:
        raise ValueError('Invalid integer cents')
    return price_cents
