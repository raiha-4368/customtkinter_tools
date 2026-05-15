import os
import csv
from pathlib import Path


#ファイル読み込み系
# *********************************************************************************
# 【Text】ファイルの読み込み
def read_text_file(filepath):
    try:
        with open(filepath, mode='r', encoding="utf-8") as f:
            return f.read(), None
    except Exception as e:
        return None, e
    
# 【Text】ファイルの読み込み(1行ずつ)
def read_line_file(filepath):
    try:
        with open(filepath, mode='r', encoding="utf-8") as f:
            return f.readlines(), None
    except Exception as e:
        return None, e

#【CSV】ファイル読み込み関数
# DictReaderを使用し、listで返す
# dict型として扱いたい場合、records[0]と記述する
def read_csv_file(filepath):
    """
    ファイルパスを受け取り、csvファイルを読み込み、その配列を返す。
    """
    records = []
    if not os.path.exists(filepath):
        return records

    with open(filepath,newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records
# *********************************************************************************

# ファイル書き込み系
# *********************************************************************************
# 【Text】ファイルへの書き込み
def write_txt_file(filepath, content):
    #新規書き込みw,追記モードaで使い分け
    with open(filepath, mode='w', newline="", encoding="utf-8") as f:
        f.write(content)
    return

# 【CSV】ファイルへの書き込み(listで書き込み)
def write_csv_file(filepath, column, content):
    #新規書き込みw,追記モードaで使い分け
    with open(filepath, mode='w', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # ヘッダー書き込み
        writer.writerow(column)
        # resultの書き込み
        for row in content:
            writer.writerow(row)
    return

# 【CSV】ファイルへの書き込み(Dict型対応)
def write_csv_file_dict(filepath, columns, content):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(content)
# *********************************************************************************


# 削除系
# *********************************************************************************
# ファイルの削除
def remove_file(filepath):
    # Pathを渡して削除する(missing_ok=Trueでファイルがなくてもエラーにしない)
    Path(filepath).unlink(missing_ok=True)
# *********************************************************************************
