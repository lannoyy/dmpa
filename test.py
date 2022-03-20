import pytest
from main import main
from error import ValidationError, AlphabetError


@pytest.mark.parametrize('str', [
    "COST = PRICE+TAX",
    "  _COST  =  (  PRICE  +  TAX  )  ",
    "COST1_1_1 = ((((PRICE+TAXeE))))*0.98e-3",
    "COST = (PRICE+TAX)*00.98e+3",
    "COST = (PRICE+TAX)*0.98e3",
    "COST = (PRICE*TAX)+0.98e-333",
    "COST == (PRICE+TAX)*0.98e-3",
    "COST = (PRICE+TAX)*0..98e-3",
    "COST = (PRICE+TAX)*0.98e-+3",
    "COST = ((PRICE+TAX)*0.98e-+3",
    "COST = (PRICE+*TAX)*0.98e+3",
    "COST = (PRICE-TAX)*0.98e-+3",
    "123",
    " ",
    "",
    "?"
])
def test(str):
    try:
        main(str)
    except ValidationError:
        assert 1
        return
    except AlphabetError:
        assert 1
        return
    except Exception:
        assert 0
    assert 1
