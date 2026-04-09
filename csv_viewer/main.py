import csv
import os
import tkinter as tk
from tkinter import filedialog,ttk
import customtkinter as ctk

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Csv_viewerApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("CSV viewer App")
        self.geometry("1200x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        #初期表示
        self.create_main_frame()

    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_main_frame(self):
        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="ファイルを開く", command=self.import_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)

        # -------------------------
        # mainフレーム内の要素
        # -------------------------
        self.filename_button = ctk.CTkButton(self.main_frame, text="ファイルを選択", command=self.import_file)
        self.filename_button.pack(pady=(20,10))
        self.filename_labl = ctk.CTkLabel(self.main_frame, text="ファイル名")
        self.filename_labl.pack(pady=(10,20))

        # Treeview
        self.treeview = ttk.Treeview(self.main_frame, show="headings")
        self.treeview.pack(expand=True,fill="both", padx=(20,20))

        # errorEntry(通常は何も表示しない、コピペ出来るようにしたいのでテキストボックスで編集不可にする)
        self.error_entry = ctk.CTkEntry(self.main_frame, width=500,
                                        state='readonly',
                                        justify="center",
                                        fg_color="transparent",
                                        border_width=0,
                                        font=("",16,"bold"),
                                        text_color="red")
        self.error_entry.pack(pady=(20,20))
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def import_file(self):

      filepath = filedialog.askopenfilename(
          defaultextension=".csv",
          filetypes=[("csv files", "*.csv"), ("All files", "*.*")],
          title="ファイルを開く"
      )
      if filepath:
        # 再びファイルを読み込んだらerrorラベルの初期化
        self.error_entry.configure(state="normal")
        self.error_entry.delete(0,tk.END)
        self.error_entry.configure(state="readonly")

        # 画面上にファイルパスを表示
        self.filename_labl.configure(text=filepath)
        
        try:
            record = load_csv(filepath)
            # 読み込めていない時は処理終了
            if not record:
                return

            # 確認用
            # print(record)
            # print("record[0]",record[0].keys())

            #1 既存データをすべて削除
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            #2 カラムの設定             
            # 以下でlist化する時、カラム行より多い要素があるとき、その列をNoneとして格納してしまう
            # columns = list(record[0].keys())
            # colがNoneの時はcolumnsに含めないよう以下とする
            columns = [col for col in record[0].keys() if col]
            
            #もしkeysにNoneを含んでいるのならflagをTrueとし、警告メッセージを表示する
            worning_flag = False
            for c in list(record[0].keys()):
                if c == None:
                    worning_flag = True

            self.treeview['columns'] = columns
            # ID列を表示しない設定
            self.treeview['show'] = 'headings'  

            # 列の見出し(ヘッダー)を設定
            for col in columns:
                self.treeview.heading(col, text=col)
                self.treeview.column(col, width=100, anchor='w')   #anchor='w'で左寄せ
            
            #データの挿入 (parent="", index="end")
            for r in record:
                # 辞書型(values)をリスト変換して渡す
                # values = [r.get(col, "-") for col in columns] r.get(col)で取得できなかった時"-"を入れるという処理⇒失敗
                values = [r.get(col) if r.get(col) is not None else "-" for col in columns]
                """
                上記処理を分解
                for col in columns:
                    if r.get(col) is not None:
                        values.append(r.get(col)) ←rに値があればその値をlistに追加
                    else:
                        values.append(r.get(-)) ←rに値がなければ-をlistに追加
                """
                self.treeview.insert("", "end", values=list(values))

            if worning_flag:
               self.error_entry.configure(state="normal")
               self.error_entry.insert(0,"WORNING:列数が一致しない行があります。")
               self.error_entry.configure(state="readonly")

        
        except Exception as e:
           self.error_entry.configure(state="normal")
           self.error_entry.insert(0,f"ERROR:{e}")
           self.error_entry.configure(state="readonly")

#csvファイル読み込み関数
def load_csv(filepath):
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


# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = Csv_viewerApp()
    #イベント待ちループ開始
    app.mainloop()

