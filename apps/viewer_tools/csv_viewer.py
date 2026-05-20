import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from common import dialogs, files

class CsvViewerApp(ctk.CTkFrame):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="CsvVirere")
        label.pack()

        # -------------------------
        # menu_frame
        # -------------------------
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack()
        # -------------------------
        # menu_frame内の要素
        # -------------------------
        self.filename_button = ctk.CTkButton(self.menu_frame, text="ファイルを選択", command=self.import_file)
        self.filename_button.pack(side="left", pady=(10,0), padx=(10,10))
        
        self.clear_button = ctk.CTkButton(self.menu_frame, text="クリア", command=self.clear)
        self.clear_button.pack(side="left", pady=(10,0), padx=(10,10))

        # -------------------------
        # content_frame
        # -------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True,fill="both")
        # -------------------------
        # content_frame内の要素
        # -------------------------
        self.filename_label = ctk.CTkLabel(self.content_frame, text="path : ")
        self.filename_label.pack(pady=(10,20))
        # Treeview
        self.treeview = ttk.Treeview(self.content_frame, show="headings")
        self.treeview.pack(expand=True,fill="both", padx=(20,20))

        # errorEntry(通常は何も表示しない、コピペ出来るようにしたいのでテキストボックスで編集不可にする)
        self.error_entry = ctk.CTkEntry(self.content_frame, width=500,
                                        state='readonly',
                                        justify="center",
                                        fg_color="transparent",
                                        border_width=0,
                                        font=("",16,"bold"),
                                        text_color="red")
        self.error_entry.pack(pady=(20,20))
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def import_file(self):

      filepath = dialogs.select_file(filetypes=[("csv files", "*.csv"), ("All files", "*.*")],title="csvファイルを選択")

      if filepath:
        # 再びファイルを読み込んだらerrorラベルの初期化
        self.error_entry.configure(state="normal")
        self.error_entry.delete(0,tk.END)
        self.error_entry.configure(state="readonly")

        # 画面上にファイルパスを表示
        self.filename_label.configure(text=filepath)
        
        try:
            record = files.read_csv_file(filepath)
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

    # クリア処理
    def clear(self):
        self.filename_label.configure(text=f"path : ")
        # 既存データをすべて削除
        for item in self.treeview.get_children():
            self.treeview.delete(item)