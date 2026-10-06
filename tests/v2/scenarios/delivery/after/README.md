# Cart

Total is the sum of integer-cent price multiplied by positive quantity plus
shipping_cents (default 0). Prices, quantities and shipping are integers;
negative prices/shipping, nonpositive quantities and empty carts are rejected.
For [(199, 2), (299, 1)] with shipping_cents=50 the total is 747 cents.
