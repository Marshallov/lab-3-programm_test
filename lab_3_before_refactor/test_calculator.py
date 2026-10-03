"""Модульные тесты для calculate_commission (ЛР №3, части 2-3)."""
import pytest

from calculator import calculate_commission


class TestPositiveScenarios:
    """Корректный расчёт комиссии для каждого тарифного диапазона."""

    @pytest.mark.parametrize("amount, expected", [
        (100, 50.0),
        (1000, 50.0),
        (1001, 100.0),
        (20000, 100.0),
        (20001, 400.01),   # 200 + 1%
        (50000, 700.0),    # 200 + 1%
    ])
    def test_commission_calculation(self, amount, expected):
        # approx нужен, т.к. 20001 * 0.01 даёт число с плавающей точкой
        assert calculate_commission(amount) == pytest.approx(expected)

    @pytest.mark.parametrize("amount, expected", [
        (500, 50.0),       # середина тарифа 1
        (10000, 100.0),    # середина тарифа 2
        (35000, 550.0),    # середина тарифа 3: 200 + 350
    ])
    def test_commission_inside_tariff_range(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected)

    def test_result_is_float(self):
        assert isinstance(calculate_commission(500), float)


class TestBoundaryValues:
    """Границы диапазонов: 100, 1000, 1001, 20000, 20001, 50000."""

    @pytest.mark.parametrize("last_in_range, first_in_next, fee_before, fee_after", [
        (1000, 1001, 50.0, 100.0),
        (20000, 20001, 100.0, 400.01),
    ], ids=["1000_to_1001", "20000_to_20001"])
    def test_tariff_switches_exactly_on_boundary(
        self, last_in_range, first_in_next, fee_before, fee_after
    ):
        assert calculate_commission(last_in_range) == pytest.approx(fee_before)
        assert calculate_commission(first_in_next) == pytest.approx(fee_after)

    @pytest.mark.parametrize("amount", [100, 50000], ids=["min_100", "max_50000"])
    def test_limits_of_valid_range_are_accepted(self, amount):
        assert calculate_commission(amount) > 0

    @pytest.mark.parametrize("amount", [99, 50001], ids=["below_min", "above_max"])
    def test_values_just_outside_valid_range_are_rejected(self, amount):
        with pytest.raises(ValueError):
            calculate_commission(amount)


class TestNegativeScenarios:
    """Обработка невалидных данных."""

    @pytest.mark.parametrize("invalid_amount", [99, 50001, -1, 0, -50000, 1000000])
    def test_out_of_range_raises_value_error(self, invalid_amount):
        with pytest.raises(ValueError):
            calculate_commission(invalid_amount)

    def test_value_error_message(self):
        with pytest.raises(ValueError, match="Сумма перевода должна быть от 100"):
            calculate_commission(99)

    @pytest.mark.parametrize("invalid_amount", ["abc", "1000", None, [100]],
                             ids=["str_abc", "str_digits", "none", "list"])
    def test_non_numeric_raises_type_error(self, invalid_amount):
        with pytest.raises(TypeError):
            calculate_commission(invalid_amount)


class TestIdempotency:
    """Функция чистая: повторный вызов даёт тот же результат."""

    @pytest.mark.parametrize("amount", [100, 1001, 20001, 50000])
    def test_repeated_calls_give_same_result(self, amount): 
        assert calculate_commission(amount) == calculate_commission(amount)
