import pytest
from project import format_lap_time, parse_round, parse_year, parse_driver, MIN_YEAR, MAX_YEAR


def test_format_lap_time():
    assert format_lap_time(65) == "1:05.000"
    assert format_lap_time(83.456) == "1:23.456"
    assert format_lap_time(119.9996) == "2:00.000"

def test_parse_year():
    assert parse_year("2026") == 2026
    assert parse_year(str(MIN_YEAR)) == MIN_YEAR
    with pytest.raises(ValueError):
        parse_year(str(MIN_YEAR - 1))
    with pytest.raises(ValueError):
        parse_year(str(MAX_YEAR + 1))
    with pytest.raises(ValueError):
        parse_year("abc")

def test_parse_round():
    assert parse_round("16", 24) == 16
    assert parse_round("1", 24) == 1
    assert parse_round("24", 24) == 24
    with pytest.raises(ValueError):
        parse_round("0", 24)
    with pytest.raises(ValueError):
        parse_round("25", 24)
    with pytest.raises(ValueError):
        parse_round("abc", 24)

def test_parse_driver():
    assert parse_driver("VER", ["VER", "LEC"]) == "VER" 
    assert parse_driver(" ver ", ["VER", "LEC"]) == "VER"
    with pytest.raises(ValueError):
        parse_driver("XYZ", ["VER", "LEC"])