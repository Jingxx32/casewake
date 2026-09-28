from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutResult:
    discounted_total_cents: int
    gift_card_debit_cents: int
    remaining_due_cents: int
    remaining_card_cents: int


def calculate_checkout(
    *, subtotal_cents: int, fixed_discount_cents: int, gift_card_balance_cents: int
) -> CheckoutResult:
    """Calculate one USD checkout using nonnegative integer-cent amounts."""
    amounts = {
        "subtotal_cents": subtotal_cents,
        "fixed_discount_cents": fixed_discount_cents,
        "gift_card_balance_cents": gift_card_balance_cents,
    }
    for name, amount in amounts.items():
        if type(amount) is not int:
            raise TypeError(f"{name} must be an integer number of cents")
        if amount < 0:
            raise ValueError(f"{name} must be nonnegative")

    discounted_total = max(subtotal_cents - fixed_discount_cents, 0)
    gift_card_debit = min(gift_card_balance_cents, discounted_total)

    return CheckoutResult(
        discounted_total_cents=discounted_total,
        gift_card_debit_cents=gift_card_debit,
        remaining_due_cents=discounted_total - gift_card_debit,
        remaining_card_cents=gift_card_balance_cents - gift_card_debit,
    )
