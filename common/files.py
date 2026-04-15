import csv
from pathlib import Path

# ファイルの読み込み
def read_text_file(filepath):
    try:
        with open(filepath, mode='r', encoding="utf-8") as f:
            return f.read(), None
    except Exception as e:
        return None, e
    
# ファイルの読み込み(1行ずつ)
def read_line_file(filepath):
    try:
        with open(filepath, mode='r', encoding="utf-8") as f:
            return f.readlines(), None
    except Exception as e:
        return None, e

# csv形式でファイルへの書き込み
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

# txt形式でファイルへの書き込み
def write_txt_file(filepath, content):
    #新規書き込みw,追記モードaで使い分け
    with open(filepath, mode='w', newline="", encoding="utf-8") as f:
        f.write(content)
    return

# ファイルの削除
def remove_file(filepath):
    # Pathを渡して削除する(missing_ok=Trueでファイルがなくてもエラーにしない)
    Path(filepath).unlink(missing_ok=True)
