import csv
from pathlib import Path
import logging

from data_contract_cli.exceptions import CSVError
from data_contract_cli.contract_models import Contract

logger = logging.getLogger(__name__)


def load_csv(path: Path, contract: Contract) -> dict:
    "load the csv file and return dict with  raw headers and raw rows."
    raw_csv_rows = []
    if not path.is_file():
        raise CSVError(f"'{path}' isn't valid file")

    if path.stat().st_size == 0:
        raise CSVError(f"'{path}' is empty")

    with open(
        path,
        "r",
        encoding=contract.encoding,
    ) as csv_file:
        content = csv.reader(csv_file, delimiter=contract.delimiter)

        for row in content:
            raw_csv_rows.append(row)

        headers = raw_csv_rows[0]
        raw_csv_rows.remove(headers)

        return {"headers": headers, "csv_rows": raw_csv_rows}


def validate_headers(raw_structure: dict, contract: Contract) -> None:
    "compare the raw headers extracts from csv and the headers from contract."
    errors = []
    headers = raw_structure["headers"]

    if not isinstance(headers, list):
        raise CSVError(f"headers: '{headers}' isn't valid")

    if len(headers) != len(set(headers)):
        raise CSVError("Column of headers isn't unique")

    if headers == contract.headers:
        return

    for column_name in contract.headers:
        if column_name not in headers:
            errors.append(column_name)
            raise CSVError(
                f"headers: '{headers}' isn't valid, their contains errors: {errors}"
            )


def is_rows_empty(raw_csv_rows: list) -> None:
    "Return an error if the rows inside the list is empty."
    flag = False
    for row in raw_csv_rows:
        for item in row:
            if item.strip() != "":
                flag = True
                return
    if flag is False:
        raise CSVError(f"csv rows is empty.")


def get_valid_rows(row: list, index: int, contract: Contract) -> dict:
    "Return a dict with valid rows, it index, and a dict with useful data."
    column_and_values = {}

    for second_index, column in enumerate(contract.headers, start=0):
        column_and_values[column] = row[second_index]

    return {"index": index, "row": row, "column_and_values": column_and_values}


def get_invalid_rows(row: list, index: int, errors: list) -> dict:
    "Return a dict with invalid row, her index and why it is invalid."

    return {"index": index, "row": row, "errors": errors}


def separate_csv_rows(contract: Contract, raw_csv_rows: list) -> dict:
    """Validate csv rows with verify length of rows, empty rows, invalid rows
    and return dict with a list of valid rows and invalid rows."""
    data_structure = {"valid_rows": [], "invalid_rows": []}
    for index, row in enumerate(raw_csv_rows, start=1):

        errors = []
        if len(row) > len(contract.headers):
            errors.append("number of columns exceeds the header.")

        if len(row) < len(contract.headers):
            errors.append("number of columns less than the header.")

        if not row:
            errors.append("row is empty.")

        if errors:
            data_structure["invalid_rows"].append(
                get_invalid_rows(row=row, index=index, errors=errors)
            )

        else:
            data_structure["valid_rows"].append(
                get_valid_rows(row=row, index=index, contract=contract)
            )
    return data_structure


def load_and_validate_csv(
    path: Path,
    contract: Contract,
) -> dict:
    logger.info(f"Started CSV structural validation: {path}")
    raw_structure = load_csv(path=path, contract=contract)
    validate_headers(raw_structure=raw_structure, contract=contract)
    raw_csv_rows = raw_structure["csv_rows"]
    is_rows_empty(raw_csv_rows)
    valid_csv = separate_csv_rows(raw_csv_rows=raw_csv_rows, contract=contract)

    if len(valid_csv["invalid_rows"]):
        logger.warning(
            "CSV structural validation completed with invalid rows: "
            f"file: {path}, "
            f"total rows: {len(raw_csv_rows)}, "
            f"valid rows: {len(valid_csv['valid_rows'])}, "
            f"invalid rows: {len(valid_csv['invalid_rows'])}, "
        )

    else:
        logger.info(
            "CSV structural validation completed successfully: "
            f"file: {path}, "
            f"total rows: {len(raw_csv_rows)}, "
            f"valid rows: {len(valid_csv['valid_rows'])}, "
            f"invalid rows: {len(valid_csv['invalid_rows'])} "
        )

    return valid_csv
