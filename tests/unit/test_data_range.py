from datetime import date

from app.core.plaining.entity import DateRange


def test_create_month_first() -> None:
    dr = DateRange.create_month(date(2020, 1, 1))
    assert dr.start == date(2020, 1, 1)
    assert dr.end == date(2020, 1, 31)


def test_create_month_last() -> None:
    dr = DateRange.create_month(date(2020, 1, 31))
    assert dr.start == date(2020, 1, 1)
    assert dr.end == date(2020, 1, 31)


def test_create_month_middle() -> None:
    dr = DateRange.create_month(date(2020, 1, 18))
    assert dr.start == date(2020, 1, 1)
    assert dr.end == date(2020, 1, 31)


def test_create_month_february_middle() -> None:
    dr = DateRange.create_month(date(2020, 2, 5))
    assert dr.start == date(2020, 2, 1)
    assert dr.end == date(2020, 2, 29)


def test_create_month_february_last() -> None:
    dr = DateRange.create_month(date(2020, 2, 29))
    assert dr.start == date(2020, 2, 1)
    assert dr.end == date(2020, 2, 29)
