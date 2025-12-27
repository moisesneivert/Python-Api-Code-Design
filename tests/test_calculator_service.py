import pytest
from app.services.calculator import calculate_average

def test_calculate_average_success():
    assert calculate_average([2, 4, 6]) == 4

def test_calculate_average_empty_list():
    with pytest.raises(ValueError):
        calculate_average([])
