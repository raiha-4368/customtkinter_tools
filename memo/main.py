import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MemoApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()
                
        self.configure(fg_color="#1a1a1a")
        self.title("Memo App *.txt")
        self.geometry("800x800")
        # -------------------------
        # ショートカット設定
        # Control-Shiftと順番が決まっている
        # 小文字のs(s)と大文字のS(Shift+s)の使い分け
        # -------------------------
        self.bind("<Control-s>", lambda e: self.update_file())
        self.bind("<Control-S>", lambda e: self.save_file())
        # mac用(動作未確認)
        # self.bind("<Command-Shift-s>", lambda e: self.save_file())

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.main_frame.pack()

        #初期表示
        self.create_widgets()
    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_widgets(self):
        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="ファイルを開く", command=self.import_file)
        file_menu.add_separator()
        file_menu.add_command(label="名前を付けて保存/Ctrl+Shift+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="上書き保存/Ctrl+s", command=self.update_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)

        # テキストエリアの作成（幅と高さを指定可能）
        # expand=True, fill="both" でウィンドウサイズに追従
        self.text_area = ctk.CTkTextbox(self.main_frame,
                                        width=800,
                                        height=1000,
                                        fg_color="#ffffff",
                                        text_color="#000000")
        self.text_area.pack(pady=(10,10),padx=(10,10),expand=True,fill="both")

        self.current_path = ""


    def save_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension = ".txt",
            filetypes=[("text files", "*.txt")],
            title="textファイルを保存"
        )

        # print(self.text_area.get("1.0", "end"))

        if filepath:
            # "end-1c"で余計な改行を削除
            content = self.text_area.get("1.0", "end-1c")

        #新規書き込みw,追記モードaで使い分け
            with open(filepath, mode='w', newline="", encoding="utf-8") as f:
                f.write(content)

          # オプション 今開いているファイル名をタイトルに表示
            self.title(f"Memo App - {filepath}")
            self.current_path = filepath

    def update_file(self):
       # selfがcurrent_pathを持っているなら処理
      if self.current_path:
        # フルパスからファイル名だけを抜き出す
        current_name = os.path.basename(self.current_path)

        # テキストエリアの記述内容を取得
        content = self.text_area.get("1.0", "end-1c")

        # ダイアログを表示⇒上書き表示の時はダイアログを表示しないよう変更
        # file_path = filedialog.asksaveasfilename(
        #    initialfile=current_name, #ここで既存ファイル名をダイアログ上に入れる
        #    defaultextension=".txt",
        #    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        #    title="名前を付けてを保存"
        # )

        # ダイアログ表示時は、ダイアログで選んだファイルパスを使用する
        # ダイアログ非表示なので、既存のファイルパスを使用する
        with open(self.current_path, mode='w', newline="", encoding="utf-8") as f:
          f.write(content)
      else:
          self.save_file()

    def import_file(self):

      filepath = filedialog.askopenfilename(
          defaultextension=".txt",
          filetypes=[("text files", "*.txt"), ("All files", "*.*")],
          title="ファイルを開く"
      )
      if filepath:
        try:
          with open(filepath, mode='r', encoding="utf-8") as f:
             content = f.read()
             # 確認用
            #  print(content)
          # テキストエリアを一度空にしてから読み込んだ内容を挿入
          self.text_area.delete("1.0", "end") #1行目から最後まで削除
          self.text_area.insert("1.0", content) #1行目に挿入

          # オプション 今開いているファイル名をタイトルに表示
          self.title(f"Memo App - {filepath}")

          # selfにファイルパスを持たせておく
          self.current_path = filepath

        except Exception as e:
           print(e)
           print("エラーが発生しました")

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = MemoApp()
    #イベント待ちループ開始
    app.mainloop()
