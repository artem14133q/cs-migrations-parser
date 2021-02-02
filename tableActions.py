import defines
import lib
import re

def dropForeignKey(migrations: dict, actionData: str):
    dropForeignKeyData = re.findall(defines.DROP_FOREIGN_KEY_PATTERN, actionData)

    dataDict = lib.parseFkName(dropForeignKeyData[0])

    column = lib.getColumn(migrations, dataDict["table"], dataDict["foreignColumn"])

    if not column:
        return migrations

    migrations[dataDict["table"]][dataDict["foreignColumn"]]["foreign"] = None

    return migrations


def dropTable(migrations: dict, actionData: str):
    tableName = lib.getDropTableData(actionData)
    
    table = migrations.get(tableName)

    if not table:
        return migrations

    migrations.pop(tableName)

    return migrations

def createTable(table: str) -> dict:
    columns = lib.getColumnsFromTable(table)

    columns = lib.appendPrimmaryKeys(columns, table)
    columns = lib.appendForeignKeys(columns, table)

    return {
        lib.getTableName(table): columns
    }

def addForeignKey(migrations: dict, actionData: str):
    foreignData = lib.getForeignData(actionData)

    column = lib.getColumn(migrations, foreignData["table"], foreignData["column"])

    if not column:
        return migrations

    column["foreign"] = {
        "table": foreignData["foreignTable"],
        "column": foreignData["foreignId"],
        "onDelete": foreignData["onDelete"]
    }

    migrations[foreignData["table"]][foreignData["column"]] = column

    return migrations

def addColumn(migrations: dict, actionData: str) -> dict:
    addColumnData = lib.getColumnData(actionData)

    table = migrations.get(addColumnData["table"])

    if not table:
        return migrations

    table.update({
        addColumnData["column"]: {
            "type": addColumnData["type"],
            "nullable": addColumnData["nullable"],
            "primary": False,
            "foreign": None
        }
    })

    migrations[addColumnData["table"]] = table

    return migrations

def dropColumn(migrations: dict, actionData: str) -> dict:
    columnData = lib.getDropColumnData(actionData)

    table = migrations.get(columnData["table"])

    if not table:
        return migrations

    column = table.get(columnData["column"])

    if not column:
        return migrations

    table.pop(columnData["column"])

    migrations[columnData["table"]] = table

    return migrations

def alterColumn(migrations: dict, actionData: str) -> dict:
    alterData = lib.getAlterColumnData(actionData)

    column = lib.getColumn(migrations, alterData["table"], alterData["column"])

    if not column:
        return migrations

    if "nullable" in alterData["alterTypes"]:
        column["nullable"] = alterData["modifys"]["nullable"]
    if "retype" in alterData["alterTypes"]:
        column["type"] = lib.mapColumnType(alterData["modifys"]["retype"])

    migrations[alterData["table"]][alterData["column"]] = column

    return migrations

def dropPrimaryKey(migrations: dict, actionData: str) -> dict:
    primaryData = lib.getDropPrimaryData(actionData)

    column = lib.getColumn(migrations, primaryData["table"], primaryData["column"])

    if not column:
        return migrations

    migrations[primaryData["table"]][primaryData["column"]]["primary"] = False

    return migrations

def renameTable(migrations: dict, actionData: str) -> dict:
    renameData = lib.getRenameTableData(actionData)

    table = migrations.get(renameData["table"])

    if not table:
        return migrations

    migrations.pop(renameData["table"])
    migrations.update({renameData["newTableName"]: table})

    return migrations

def addPrimaryKey(migrations: dict, actionData: str) -> dict:
    addPrimaryData = lib.getAddPrimaryKeyData(actionData)

    column = lib.getColumn(migrations, addPrimaryData["table"], addPrimaryData["column"])

    if not column:
        return migrations

    migrations[addPrimaryData["table"]][addPrimaryData["column"]]["primary"] = True

    return migrations

def renameColumn(migrations: dict, actionData: str) -> dict:
    renameColumnData = lib.getRenameColumnData(actionData)

    column = lib.getColumn(migrations, renameColumnData["table"], renameColumnData["column"])

    if not column:
        return migrations

    migrations[renameColumnData["table"]].pop(renameColumnData["column"])
    migrations[renameColumnData["table"]].update({
        renameColumnData["newColumnName"]: column
    })

    return migrations
