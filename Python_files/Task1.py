import pandas as pd
import sqlite3


def openExcelFile(file_name: str, card: str) -> list:
    """
    Opens .xlsx file and put it to list.
    Parameters:
    - file_name: name of the file
    - card: name of the card (Visa or Mastercard)
    Returns:
     - list where every element is a row from the xlsx file
    """
    xlsx_file = pd.ExcelFile(file_name).parse(card)
    df = pd.DataFrame(xlsx_file, columns= xlsx_file.keys())
    data = [df.columns.values.tolist()] + df.values.tolist()
    return data


def openSQLiteFile(file_name: str) -> sqlite3.Cursor:
    """
    Opens .sqlite file.
    Parameters:
    - file_name: name of the file
    Returns:
     - sqlite3 cursor
    """
    con = sqlite3.connect(file_name)
    cursor = con.cursor()
    return cursor


def match_chargebacks(xlsx_data: list, sqlite_data: sqlite3.Cursor) -> list:
    """
    Matching xlsx file with sqlite file.
    Parameters:
    - xlsx_data: data from xlsx file
    - sqlite_data: data from sqlite file
    Returns:
     - list of transactions id
    """
    sqlite_data = [a for a in sqlite_data]
    id_list = []
    for report in xlsx_data:
        date = report[0]
        for row in sqlite_data:
            if date == row[1]:
                id_list.append(row[0])
    return id_list


def reports(card: str) -> list:
    """
    Returns a list of reported transaction id of the given card brand
    Parameters:
    - card: card brand
    Returns:
     - list of transactions id
    """
    cursor = openSQLiteFile("db.sqlite")
    sqlite_data = cursor.execute(f'SELECT "transactions"."id", "transactions"."created_at" \
                                 FROM transactions, cards \
                                 WHERE "transactions"."card_id" = "cards"."id" \
                                 AND "cards"."brand" = "{card.lower()}"')
    xlsx_file = openExcelFile("Processing Report.xlsx", card)
    reports = match_chargebacks(xlsx_file, sqlite_data)
    return reports


if __name__ == "__main__":
    with open("reported_id.txt", "w") as file:
        visa = reports("Visa")
        print(f"Visa reported id ({len(visa)}):", file=file)
        [print(id, file=file) for id in visa]
        mastercard = reports("Mastercard")
        print(f"Mastercard reported id ({len(mastercard)}):", file=file)
        [print(id, file=file) for id in mastercard]
