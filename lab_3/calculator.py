"""Модуль «Калькулятор комиссий» (версия после рефакторинга, ЛР №3)."""

MIN_AMOUNT = 100
MAX_AMOUNT = 50_000

TARIFF_1_LIMIT = 1_000        # до суммы включительно — тариф 1
TARIFF_2_LIMIT = 20_000       # до суммы включительно — тариф 2
FIXED_FEE_THRESHOLD = 40_000  # строго больше — фиксированная комиссия

TARIFF_1_FEE = 50.0
TARIFF_2_FEE = 100.0
TARIFF_3_BASE_FEE = 200.0
TARIFF_3_RATE = 0.01
FIXED_FEE = 500.0


def _format_rub(value: int) -> str:
    """Разделяет разряды пробелами: 50000 -> '50 000'."""
    return f"{value:,}".replace(",", " ")


def _validate_amount(amount: int) -> None:
    """Проверяет тип и диапазон суммы перевода."""
    # bool — подкласс int, но True/False не являются суммой перевода
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise TypeError(
            f"Сумма перевода должна быть целым числом, получено: {type(amount).__name__}"
        )
    if not MIN_AMOUNT <= amount <= MAX_AMOUNT:
        raise ValueError(
            f"Сумма перевода должна быть от {_format_rub(MIN_AMOUNT)} "
            f"до {_format_rub(MAX_AMOUNT)} руб."
        )


def calculate_commission(amount: int) -> float:
    """
    Рассчитывает комиссию для денежного перевода.

    Тарифы:
        100 – 1 000 руб.        -> 50 руб.
        1 001 – 20 000 руб.     -> 100 руб.
        20 001 – 40 000 руб.    -> 200 руб. + 1% от суммы
        свыше 40 000 руб.       -> 500 руб. (фиксированная комиссия)

    Args:
        amount (int): Сумма перевода (от 100 до 50 000 руб.)

    Returns:
        float: Размер комиссии

    Raises:
        TypeError: Если сумма не является целым числом
        ValueError: Если сумма не входит в допустимый диапазон
    """
    _validate_amount(amount)

    if amount <= TARIFF_1_LIMIT:
        return TARIFF_1_FEE
    if amount <= TARIFF_2_LIMIT:
        return TARIFF_2_FEE
    if amount <= FIXED_FEE_THRESHOLD:
        # round убирает артефакты float: 200 + 20001 * 0.01 -> ровно 400.01
        return round(TARIFF_3_BASE_FEE + amount * TARIFF_3_RATE, 2)
    return FIXED_FEE
