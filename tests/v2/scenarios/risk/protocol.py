"""Evaluation fixture with a real configuration emitter and consumer."""
def emit(total_cents, currency):
    if type(total_cents) is not int or total_cents < 0 or currency not in ('USD', 'EUR'):
        raise ValueError('Invalid receipt')
    return {'cents': total_cents, 'currency': currency}


def consume(receipt):
    checked = emit(receipt['cents'], receipt['currency'])
    cents = checked['cents']
    return f"{checked['currency']} {cents // 100}.{cents % 100:02d}"


def broken_consumer(receipt):
    emit(receipt['cents'], receipt['currency'])  # parsed but not used
    return f"USD {receipt['cents'] // 100}.{receipt['cents'] % 100:02d}"
