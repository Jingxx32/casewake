# Checkout calculation rules

The demo uses one currency, USD. Every input and output is an integer number of cents. There is no currency conversion or fractional-cent rounding.

1. The subtotal, fixed discount, and gift-card balance must each be a nonnegative integer. Reject booleans, decimal values, strings, and negative amounts.
2. Apply the fixed discount before using the gift card. If the discount exceeds the subtotal, the discounted total is zero; there is no credit or negative order value.
3. Debit the gift card by the smaller of its balance and the discounted total. The card cannot be overdrawn.
4. Any part of the discounted total not covered by the gift card remains due. The unused gift-card balance remains on the card.

The first version excludes tax, shipping, percentage discounts, multiple gift cards, and multiple currencies. It computes a result without charging a card or changing stored state.

| Subtotal | Discount | Card balance | Discounted total | Card debit | Remaining due | Card remaining |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $100.00 | $20.00 | $80.00 | $80.00 | $80.00 | $0.00 | $0.00 |
| $100.00 | $20.00 | $100.00 | $80.00 | $80.00 | $0.00 | $20.00 |
| $100.00 | $20.00 | $50.00 | $80.00 | $50.00 | $30.00 | $0.00 |
