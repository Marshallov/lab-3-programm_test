"""Модуль «Калькулятор комиссий» (исходная версия из ЛР №1)."""


def calculate_commission(amount: int) -> float:
    """
    Рассчитывает комиссию для денежного перевода.

    Args:
        amount (int): Сумма перевода (от 100 до 50 000 руб.)

    Returns:
        float: Размер комиссии

    Raises:
        ValueError: Если сумма не входит в допустимый диапазон
    """
    if amount < 100 or amount > 50000:
        raise ValueError("Сумма перевода должна быть от 100 до 50 000 руб.")

    if amount <= 1000:
        return 50.0
    elif amount <= 20000:
        return 100.0
    else:
        return 200.0 + (amount * 0.01)
