DUMP_DIR = "./dumps"

DISABLE_ACTIONS = [
    "CreateIndex",
    "RenameIndex",
    "DropIndex",
    "UpdateData",
    "InsertData",
    "DeleteData",
    "Sql"
]

TYPES_MAP = {
    "long": "bigIntrger",
    "decimal": "integer",
    "Guid": "string",
    "DateTime": "dateTime",
    "int": "integer"
}

ACTIONS_PATTERN = r"migrationBuilder\.(\w+)"

TABLE_NAME_PATTERN = r"name:\s*\"(\w+)\",\s+columns"

CAMEL_CASE_NAMES_PATTRN = r"[A-Za-z][a-z]+|[A-Z]+|\d+"

ACTION_TABLE_PATTERN = r"migrationBuilder\.(\w+)([\S\s]+?)(?=migrationBuilder)"

COLUMN_DATA_PATTERN = r"\s*(\w+)\s=\stable\.Column<(\w+)>\(nullable:\s(\w+)"

PRIMARY_KEYS_RAW_PATTERN = r"table\.PrimaryKey[^;]+"

PRIMARY_KEYS_PATTERN = r"{?,? \w\.(\w+)"

FOREIGN_KEYS_PATTERN = r"ForeignKey[^.]+\.(\w+)[^.]+?[^\"]+\"(\w+)\"[^\"]+\"(\w+)\"[^.]+.(\w+)"

ADD_FOREIGN_KEY_PATTERN = r"table:\s*\"(\w*)\"[^\"]+\"(\w+)\"[^\"]+\"(\w+)\"[^\"]+\"(\w+)\"[^\.]+.(\w+)"

DROP_TABLE_PATTERN = r"name:\s*\"(\w+)\""

DROP_FOREIGN_KEY_PATTERN = r"(\w+)\","

ADD_COLUMN_PATTERN = r"<(\w+)>[^\"]+\"(\w+)\"[^\"]+\"(\w+)\"[\S\s]+?nullable:\s*(\w+)"

DROP_COLUMN_PATTERN = r"(\w+)\"[^\"]+\"(\w+)"

ALTER_TABLE_COLUMN_DATA_PATTERN = r"<\w+>[^\"]+\"(\w+)\"[^\"]+\"(\w+)"

ALTER_TABLE_NULLABLE_PATTERN = r"nullable:\s*(\w*)"

ALTER_TABLE_TYPE_PATTERN = r"type:\s*\"(\w+)"

DROP_PRIMARY_KEY_PATTERN = r"table:\s*\"(\w+)\",\s*column:\s*\"(\w+)\""

RENAME_PATTERN = r"\"(\w+)\""

ADD_PRIMARY_KEY_DATA = r"table:\s*\"(\w+)\"[^\"]+\"(\w+)"