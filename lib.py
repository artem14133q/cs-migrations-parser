import defines
import re

def mapColumnType(name: str) -> str:
    type = defines.TYPES_MAP.get(name)

    return type if type else name

def isNullable(null: str) -> bool:
    return True if null == "true" else False

def prepareName(name: str) -> str:
    nameList = re.findall(defines.CAMEL_CASE_NAMES_PATTRN, name)

    return "_".join(
        list(
            map(lambda x: x.lower(), nameList)
        )
    )

def appendForeignKeys(columns: dict, table: str) -> dict:
    fkKeys = re.findall(defines.FOREIGN_KEYS_PATTERN, table)

    fkData = {}

    for key in fkKeys:
        fkData.update({ prepareName(key[0]): {
                "table": prepareName(key[1]),
                "column": prepareName(key[2]),
                "onDelete": key[3].upper()
            }
        })

    columnsWithFk = {}

    for key, column in columns.items():
        column["foreign"] = fkData.get(key)
        columnsWithFk.update({key: column})

    return columnsWithFk

def appendPrimmaryKeys(columns: dict, table: str) -> dict:
    pkRaw = re.findall(defines.PRIMARY_KEYS_RAW_PATTERN, table)
    pkKeys = re.findall(defines.PRIMARY_KEYS_PATTERN, pkRaw[0])

    pkKeys = list(
        map(lambda x: prepareName(x.lower()), pkKeys)
    )

    columnsWithPrimary = {}

    for key, column in columns.items():
        column["primary"] = key in pkKeys

        columnsWithPrimary.update({key: column})

    return columnsWithPrimary

def getColumnsFromTable(table: str) -> list:
    columns = re.findall(defines.COLUMN_DATA_PATTERN, table)

    formatColumns = {}
    
    for column in columns:
        formatColumns.update({
            prepareName(column[0]): {
                "type": mapColumnType(column[1]),
                "nullable": isNullable(column[2])
            }
        })

    return formatColumns

def getTableName(table: str) -> str:
    names = re.findall(defines.TABLE_NAME_PATTERN, table)

    return prepareName(names[0])

def dump(name: str, data: str):
    with open(defines.DUMP_DIR + "/" + name, "w") as writeFile:
        writeFile.write(data)

def getForeignData(actionData: str) -> str:
    foreign = re.findall(defines.ADD_FOREIGN_KEY_PATTERN, actionData)[0]

    return {
        "table": prepareName(foreign[0]),
        "column": prepareName(foreign[1]),
        "foreignTable": prepareName(foreign[2]),
        "foreignId": prepareName(foreign[3]),
        "onDelete": foreign[4].upper()
    }

def getColumn(migrations: dict, tableName: str, columnName: str) -> dict or None:
    table = migrations.get(tableName)

    if not table:
        return None

    column = table.get(columnName)

    if not column:
        return None

    return column

def parseFkName(name: str) -> dict:
    nameList = name.split("_")

    nameList = list(
        map(lambda x: prepareName(x), nameList[1:])
    )

    return {
        "table": nameList[0],
        "foreignTable": nameList[1],
        "foreignColumn": nameList[2]
    }

def getColumnData(actionData: str) -> dict:
    addColumnData = re.findall(defines.ADD_COLUMN_PATTERN, actionData)[0]

    return {
        "type": mapColumnType(addColumnData[0]),
        "column": prepareName(addColumnData[1]),
        "table": prepareName(addColumnData[2]),
        "nullable": isNullable(addColumnData[3])
    }

def getDropColumnData(actionData: str) -> dict:
    dropColumnData = re.findall(defines.DROP_COLUMN_PATTERN, actionData)[0]

    return {
        "column": prepareName(dropColumnData[0]),
        "table": prepareName(dropColumnData[1])
    }

def getAlterColumnData(actionData: str) -> dict or None:
    columnData = re.findall(defines.ALTER_TABLE_COLUMN_DATA_PATTERN, actionData)[0]
    nullableData = re.findall(defines.ALTER_TABLE_NULLABLE_PATTERN, actionData)
    retypeData = re.findall(defines.ALTER_TABLE_TYPE_PATTERN, actionData)

    if not nullableData and not retypeData:
        return None

    alterTypes = []
    modifys = {}

    if nullableData:
        alterTypes.append("nullable")
        modifys.update({"nullable": isNullable(nullableData[0])})
    if retypeData:
        alterTypes.append("retype")
        modifys.update({"retype": mapColumnType(retypeData[0])})

    return {
        "column": prepareName(columnData[0]),
        "table": prepareName(columnData[1]),
        "alterTypes": alterTypes,
        "modifys": modifys
    }

def getDropPrimaryData(actionData: str):
    primaryData = re.findall(defines.DROP_PRIMARY_KEY_PATTERN, actionData)[0]

    return {
        "table": prepareName(primaryData[0]),
        "column": prepareName(primaryData[1])
    }

def getRenameTableData(actionData: str) -> dict:
    renameData = re.findall(defines.RENAME_PATTERN, actionData)

    return {
        "table": prepareName(renameData[0][0]),
        "newTableName": prepareName(renameData[1][0])
    }

def getAddPrimaryKeyData(actionData: str) -> dict:
    addPrimaryData = re.findall(defines.ADD_PRIMARY_KEY_DATA, actionData)[0]

    return {
        "table": prepareName(addPrimaryData[0]),
        "column": prepareName(addPrimaryData[1])
    }

def getRenameColumnData(actionData: str):
    renameColumnData = re.findall(defines.RENAME_PATTERN, actionData)

    return {
        "column": prepareName(renameColumnData[0]),
        "table": prepareName(renameColumnData[1]),
        "newColumnName": prepareName(renameColumnData[2])
    }

def getDropTableData(actionData: str) -> str:
    dropTableData = re.findall(defines.DROP_TABLE_PATTERN, actionData)

    return prepareName(dropTableData[0])