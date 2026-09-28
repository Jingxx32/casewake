import pytest

from demo_app.checkout import CheckoutResult, calculate_checkout


@pytest.mark.parametrize(
    ("card_balance", "expected"),
    [
        (8000, CheckoutResult(8000, 8000, 0, 0)),
        (10000, CheckoutResult(8000, 8000, 0, 2000)),
        (5000, CheckoutResult(8000, 5000, 3000, 0)),
    ],
)
def test_discount_applies_before_gift_card(card_balance: int, expected: CheckoutResult) -> None:
    assert calculate_checkout(
        subtotal_cents=10000,
        fixed_discount_cents=2000,
        gift_card_balance_cents=card_balance,
    ) == expected


def test_discount_above_subtotal_does_not_create_a_credit() -> None:
    assert calculate_checkout(
        subtotal_cents=500,
        fixed_discount_cents=700,
        gift_card_balance_cents=1000,
    ) == CheckoutResult(0, 0, 0, 1000)


def test_no_discount_or_gift_card_leaves_full_amount_due() -> None:
    assert calculate_checkout(
        subtotal_cents=1000,
        fixed_discount_cents=0,
        gift_card_balance_cents=0,
    ) == CheckoutResult(1000, 0, 1000, 0)


@pytest.mark.parametrize("field", ["subtotal_cents", "fixed_discount_cents", "gift_card_balance_cents"])
def test_negative_amount_is_rejected(field: str) -> None:
    amounts = {"subtotal_cents": 100, "fixed_discount_cents": 20, "gift_card_balance_cents": 80}
    amounts[field] = -1

    with pytest.raises(ValueError, match=field):
        calculate_checkout(**amounts)


@pytest.mark.parametrize("invalid", [True, 1.5, "100"])
def test_non_integer_cents_are_rejected(invalid: object) -> None:
    with pytest.raises(TypeError, match="subtotal_cents"):
        calculate_checkout(
            subtotal_cents=invalid,
            fixed_discount_cents=20,
            gift_card_balance_cents=80,
        )
