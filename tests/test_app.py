# tests/test_app.py
import pytest
from app import add, sub, mul, div, parse_and_run

def test_add():
    assert add(2, 3) == 5

def test_sub():
    assert sub(5, 3) == 2

def test_mul():
    assert mul(3, 4) == 12

def test_div():
    assert div(10, 2) == 5

def test_div_float():
    assert div(7, 2) == 3.5

def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        div(1, 0)

def test_parse_and_run_add():
    assert parse_and_run(["app.py", "add", "2", "3"]) == 5.0

def test_parse_and_run_invalid_op():
    with pytest.raises(ValueError):
        parse_and_run(["app.py", "pow", "2", "3"])

def test_parse_and_run_bad_args():
    with pytest.raises(ValueError):
        parse_and_run(["app.py", "add", "two", "3"])
