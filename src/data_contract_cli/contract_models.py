class Columns_Contract:
    def __init__(
        self,
        column_name: str,
        column_type: str,
        required: bool = False,
        nullable: bool = False,
        unique: bool = False,
        rules: dict = {},
        transformations: list = [],
    ) -> None:
        self.column_name = column_name
        self.column_type = column_type
        self.required = required
        self.nullable = nullable
        self.unique = unique
        self.rules = rules
        self.transformations = transformations

    def __repr__(self) -> str:
        return (
            f"\ncolumn_name: '{self.column_name}',\n"
            f"column_type: '{self.column_type}', \n"
            f"required: {self.required},\n"
            f"nullable: {self.nullable}, \n"
            f"unique: {self.unique}, \n"
            f"rules : {self.rules}\n"
            f"transformations: {self.transformations},\n"
            f"\n"
        )


class Contract:
    def __init__(
        self,
        columns: dict,
        headers: list,
        delimiter: str = ",",
        encoding: str = "utf-8",
    ) -> None:
        self.columns = columns
        self.headers = headers
        self.delimiter = delimiter
        self.encoding = encoding

    def __repr__(self) -> str:
        return (
            f"Delimiter: '{self.delimiter}',\n"
            f"Encoding: '{self.encoding}',\n"
            f"Headers: {self.headers},\n"
            f"Columns:\n{self.columns}"
        )
