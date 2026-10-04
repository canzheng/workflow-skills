"""Cross-module CLI pilot: execute cart config and format its actual result."""
import json
import sys
from cart import total


def receipt(lines, shipping_cents, currency):
    if currency not in ('USD', 'EUR'):
        raise ValueError('Unsupported currency')
    cents = total(lines, shipping_cents)
    return f'{currency} {cents // 100}.{cents % 100:02d}'


if __name__ == '__main__':
    try:
        request = json.load(sys.stdin)
        print(receipt(request['lines'], request.get('shipping_cents', 0), request['currency']))
    except (ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
