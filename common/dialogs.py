import tkinter as tk
from tkinter import filedialog

# ファイル選択ダイアログ
def select_file(filetypes=(("All Files", " * "),), title="ファイルを開く") -> str:  # type hint: 戻り値の戻り値の想定
      root = tk.Tk()
      root.withdraw() # メインウィンドウ非表示

      filepath = filedialog.askopenfilename(filetypes=filetypes,title=title)

      root.destroy()
      return filepath

# フォルダ選択ダイアログ
def select_folder(title="フォルダを開く") -> str: # type hint: 戻り値の戻り値の想定
      root = tk.Tk()
      root.withdraw() # メインウィンドウ非表示

      folder_path = filedialog.askdirectory(title=title)

      root.destroy()
      return folder_path

# txtファイルの場合
def select_text_file():
  return select_file(filetypes=(("Text Files", "*.txt"),),title="txtファイルを開く")


# csvファイルとして保存
def save_csv_file(filetypes=(("csv files", "*.csv"),), title="ファイル保存", filename="text_extract_output.csv") -> str:
      root = tk.Tk()
      root.withdraw() # メインウィンドウ非表示

      filepath = filedialog.asksaveasfilename(
      defaultextension = ".csc",
      initialfile=filename, 
      filetypes=filetypes,
      title=title
      )
      root.destroy()
      return filepath
