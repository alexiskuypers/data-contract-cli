from data_contract_cli.contract_models import Contract, Columns_Contract
import pytest


def test_contract_object():
    column = Columns_Contract(
        column_name="id",
        column_type="str",
        required=True,
        nullable=False,
        unique=False,
        rules={},
        transformations=["strip", "collapse_spaces", "title"],
    )
    columns = {"id": column}

    contract = Contract(
        delimiter=",", encoding="utf-8", headers=["id"], columns=columns
    )
    assert contract.delimiter == ","
    assert isinstance(contract.columns, dict) == True
    assert isinstance(contract.columns["id"], Columns_Contract) == True
    assert contract.headers == ["id"]
    assert contract.encoding == "utf-8"


def test_columns_contract_object():
    column = Columns_Contract(
        column_name="id",
        column_type="str",
        required=True,
        nullable=False,
        unique=False,
        rules={},
        transformations=["strip", "collapse_spaces", "title"],
    )
    assert column.column_name == "id"
    assert column.column_type == "str"
    assert column.required is True
    assert column.nullable is False
    assert column.unique is False
    assert column.rules == {}
    assert column.transformations == ["strip", "collapse_spaces", "title"]
