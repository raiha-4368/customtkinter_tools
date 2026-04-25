import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
from common import dialogs
import logging
from logging.handlers import RotatingFileHandler
import sqlite3

SELECT_QUERY ="""SELECT * {tablename}"""

#tableの一覧表示
TABLE_LIST = """SELECT name
              FROM sqlite_master
              WHERE type = 'table'
              ORDER BY name;"""

# テーブル構造の把握用
TABLE_PRAGMA = "PRAGMA table_info({table_name});"

# =====================================
# 実行ディレクトリを取得
# =====================================
def get_base_path():
    if getattr(sys,'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# =====================================
# logs及びDBディレクトリを作成
# =====================================
def mkdir_logs_db():
    base_path = get_base_path()
    
    log_dir = os.path.join(base_path, "logs")
    db_dir = os.path.join(base_path, "db")

    # フォルダが既に存在していてもエラーにはならない
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(db_dir, exist_ok=True)

    log_path= os.path.join(log_dir, "app.log")
    db_path= os.path.join(db_dir, "torelog.db")
    
    return log_path, db_path


#======================================
# logging 設定
#======================================
#ディレクトリがなければ作成
mkdir_logs_db()
# Logger 作成
logger = logging.getLogger("resale_app")
logger.setLevel(logging.INFO)

# handler 作成
log_handler = RotatingFileHandler(
        "apps/db_viewer/logs/app.log",
        maxBytes = 1024 * 1024, # 1MBでローテーション
        backupCount = 3,        # 古いログを3世代保持
        encoding = "utf-8"
    )

# formatter
log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
log_handler.setFormatter(log_formatter)

# handler 登録(重複防止)
if not logger.handlers:
    logger.addHandler(log_handler)


# =====================================
# DBへの接続、SQLの実行を行う
# =====================================
def query_exe(sql, db_path,placeholder=None, fetch=False):
    logger.info("query_exe: falepath=%s", db_path)
    conn = sqlite3.connect(db_path)
    try:
        #辞書型設定
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        #placeholderがTrueならそのまま、Falseなら空を渡す
        cursor.execute(sql,placeholder or ())
        if fetch:
        # memo
        #fetchone() 1件だけ
        #fetchall() 全件
            return cursor.fetchall()
        else:
        #commitはselect文には不要のため分岐処理
            conn.commit()
            return None
    finally:
        conn.close()
# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class DB_ViewerApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#191919")
        self.title("DB_Viewer App")
        self.geometry("1500x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        # self.main_frame = ctk.CTkFrame(self, fg_color="#191919")
        # self.main_frame.pack(fill="both", expand=True)

        # self.table_list_frame = ctk.CTkFrame(self, fg_color="#191919")
        # self.table_list_frame.pack(fill="both", expand=True)

        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)

        # コンテナ（全てのフレームを置く場所）
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.state_map = {
            "db_path": "",
            "tables": [],
            "selected_table": "",
            "query_result": [],
            "table_structure": []
        }
        

        # 画面の登録
        for F in (SelectPage, SqlPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectPage")

    def show_frame(self, page_name):
        # 画面を呼び出す直前に更新処理を入れることも可能
        frame = self.frames[page_name]
        if hasattr(frame, "update_label"): # 更新用メソッドがあれば実行
            frame.update_label()
        frame.tkraise()

# -------------------------
# メイン画面表示UI
# -------------------------
class SelectPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # クラス内で参照可能にする
        self.controller = controller

        # ***************************************************************************************************
        # about_frame
        self.about_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.about_frame.pack()
    
        # ファイル選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.about_frame,text="■dbファイルの中身をチェックします")
        self.folder_label.pack()
        # # 開始位置を揃える設定 →中身を左に寄せる:anchor="w" ,横幅いっぱいに広げる:fill="x"
        self.folder_label2 = ctk.CTkLabel(self.about_frame,text="・dbファイル選択後、table一覧を表示します。",anchor="w")
        self.folder_label2.pack(fill="x")
        self.folder_label3 = ctk.CTkLabel(self.about_frame,text="・tableを選択することで対象にselect文を実行します",anchor="w")
        self.folder_label3.pack(fill="x")

        # ***************************************************************************************************
        # select_frame
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame.pack()

        # ファイル選択を行うボタン
        self.file_button = ctk.CTkButton(self.select_frame, text="ファイルを選択", command=self.select_file, anchor="w")
        self.file_button.pack(side="left", pady=(10,10),padx=(0,10), fill="x")

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.select_frame, text="path:", width=500, anchor="w")
        self.dir_path.pack(side="left",pady=(10,10),fill="x")
        # ***************************************************************************************************

    # ファイルを開く
    def select_file(self):
        state = self.controller.state_map
        # ファイルを選択
        filepath = dialogs.select_file()

        if filepath:
            try:
                # dbファイルに対してテーブル一覧を取得するsqlの実行
                result = query_exe(TABLE_LIST,filepath, fetch=True)
                
                # sqlの結果resultから1つずつ取り出してリスト化
                table_list = [row[0] for row in result]

                # stateに保存 
                # 親クラス(app)に持たせる
                state['db_path'] = filepath
                state['tables'] = table_list

                # 画面上にパスを表示
                self.dir_path.configure(text=filepath)

                self.controller.show_frame("SqlPage")

            except Exception as e:
                  messagebox.showerror("エラー",e)



    # -------------------------
    # テーブル一覧表示用
    # -------------------------
class SqlPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # クラス内で参照可能にする
        self.controller = controller

        self.db_path = ""
        
        
        # ***************************************************************************************************
        # select_frame frameを左寄せにする
        self.sql_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sql_frame.pack()

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.sql_frame, text=f"path:", width=500, anchor="w")
        self.dir_path.pack(pady=(10,10),fill="x")

        # SQLの入力欄
        self.sql_label = ctk.CTkLabel(self.sql_frame, text="SQL:このページではCREATE TABLEのsqlの実行をしてください",width=500, anchor="w")
        self.sql_label.pack(pady=(10,10),fill="x")

        self.sql_command = ctk.CTkTextbox(self.sql_frame,width=500, font=("Meiryo", 20))
        self.sql_command.pack(pady=(10,10))

        self.start_sql = ctk.CTkButton(self.sql_frame, text="実行",command=self.textbox_sql)
        self.start_sql.pack(pady=(10,10))
        # ***************************************************************************************************

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        # テーブルの一覧
        self.table_list = ctk.CTkScrollableFrame(self.list_frame, label_text="選択フォルダ内のテーブルリスト")
        self.table_list.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # ***************************************************************************************************
        
        # ***************************************************************************************************
        # button_frame
        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.button_frame.pack()

        # ***************************************************************************************************
        # 切り替え
        ctk.CTkButton(self.button_frame, text="戻る", 
                      command=lambda: controller.show_frame("SelectPage")).pack()

        # ***************************************************************************************************

    # 画面切り替え時の画面更新
    def update_label(self):
        state = self.controller.state_map
        # 画面のパス更新
        self.dir_path.configure(text=f"{state['db_path']}")
        # テキストボックスを1行目から最後まで削除
        self.sql_command.delete("1.0", "end")

        # listboxに値を入れる
        self.update_listbox()


    def textbox_sql(self):
        state = self.controller.state_map

        # テキストエリアの記述内容を取得
        content = self.sql_command.get("1.0", "end-1c")
        if content:
            try:
                # dbファイルに対してテーブル一覧を取得するsqlの実行
                query_exe(content,state['db_path'])

                messagebox.showinfo("sqlを実行しました", f"{content}を実行しました")
                self.update_listbox()

            except Exception as e:
                  messagebox.showerror("エラー",e)

    def update_listbox(self):
        state = self.controller.state_map

        # リスト用のボタン削除
        for child in self.table_list.winfo_children():          
            child.destroy()

        # スクロールラベルバーにボタンを追加
        # 押下された際はtableを引数に持ち、select_table関数へ遷移
        for t in state['tables']:
            btn = ctk.CTkButton(self.table_list,
                                text=t,
                                fg_color="#FFFFFF",
                                text_color="#000000",
                                anchor="w",
                                command=lambda table=t: self.select_table(table))
            btn.pack(fill="x")

    def select_table(self, table):
        state = self.controller.state_map

        state['selected_table'] = table

        # SELECT実行
        sql = f"SELECT * FROM {table}"
        result = query_exe(sql, state["db_path"], fetch=True)
        print("result:",result)
        state["query_result"] = result

        # teble構造を取得
        pragma_sql = f"PRAGMA table_info({table});"
        structure = query_exe(pragma_sql, state['db_path'], fetch=True)
        state['table_structure'] = structure

        self.controller.show_frame("ResultPage")

        
    # -------------------------
    # テーブル一覧表示用
    # -------------------------
class ResultPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
                
        # クラス内で参照可能にする
        self.controller = controller

        self.db_path = ""
        
        # ***************************************************************************************************
        # select_frame frameを左寄せにする
        self.sql_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sql_frame.pack()

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.sql_frame, text=f"DBファイルpath:", width=500, anchor="w")
        self.dir_path.pack(pady=(10,10),fill="x")

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.treename_lable = ctk.CTkLabel(self.list_frame, text="テーブル構造")
        self.treename_lable.pack(padx=(20,20),pady=(20,20))

        # Treeview
        self.treeview = ttk.Treeview(self.list_frame, show="headings")
        self.treeview.pack(padx=(20,20))
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treename_lable2 = ctk.CTkLabel(self.list_frame, text="テーブル内データ")
        self.treename_lable2.pack(padx=(20,20),pady=(20,20))

        # Treeview2
        self.treeview2 = ttk.Treeview(self.list_frame, show="headings")
        self.treeview2.pack(padx=(20,20))
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.treeview.yview)
        self.treeview2.configure(yscrollcommand=scrollbar.set)

        style = ttk.Style()
        # テーマ設定(後で設定すると上書きされる)
        style.theme_use("default")
        # 見出し部分のフォント変更
        style.configure("Treeview.Heading",
                        font=("Meirio", 20, "bold"),     # フォントタイプ、文字サイズ
                        background="#323232",          # 全体の背景色
                        foreground="white")              # 文字の色
        
        # データ部分のフォントサイズ変更
        style.configure("Treeview",
                        font=(None, 16),                # フォントタイプ、文字サイズ
                        background="#696969",         # 全体の背景色
                        foreground="white",             # 文字の色
                        fieldbackground="#808080")   # データがない部分の色

        # 選択時の色
        style.map("Treeview",
                  background=[('selected', "#347083")],
                  foreground=[("selected", 'white')])


        # 特定行のみ色を変える例
        # # 1. タグに色を設定しておく
        # tree.tag_configure('alert', background='red', foreground='white')
        # tree.tag_configure('even', background='#e1e1e1')

        # # 2. データを追加する時に、そのタグを割り当てる
        # tree.insert("", "end", values=("001", "重要データ"), tags=("alert",))
        # tree.insert("", "end", values=("002", "通常データ"), tags=("even",))

        # ストライプの表の例
        # for i in range(10):
        #     tag = "even" if i % 2 == 0 else "odd"
        #     tree.insert("", "end", values=(i, "データ"), tags=(tag,))

        #     tree.tag_configure("even", background="#ffffff")
        #     tree.tag_configure("odd", background="#f9f9f9")

        # # テーブル情報の表示
        # self.table_list = ctk.CTkScrollableFrame(self.list_frame, label_text="テーブル構造とSELECT結果")
        # self.table_list.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # ***************************************************************************************************

        # ***************************************************************************************************
        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.button_frame.pack()# 切り替え
        ctk.CTkButton(self.button_frame, text="戻る", 
                      command=lambda: controller.show_frame("SqlPage")).pack(padx=(20,20),pady=(20,20))
        # ***************************************************************************************************

    # 画面切り替え時の画面更新
    def update_label(self):
        state = self.controller.state_map
        # 画面のパス更新
        self.dir_path.configure(text=f"DBファイルpath:{state['db_path']}")
        # listboxに値を入れる
        self.update_listbox()
    
    def update_listbox(self):
        # # リスト用のボタン削除
        # for child in self.table_list.winfo_children():          
        #     child.destroy()

        self.show_structure()

        self.show_data()

    # 構造表示用メソッド
    def show_structure(self):
        state = self.controller.state_map
        structure =state['table_structure']

        if not structure:
            return

        # textboxへの処理はコメントアウト        
        # # 見出し
        # header = ctk.CTkLabel(self.table_list, text=f"---  {state['selected_table']}テーブル構造  ---", anchor="w")
        # header.pack(fill="x")

        # for col in structure:
        #     text = f"{col['name']} ({col['type']})"
        #     label = ctk.CTkLabel(self.table_list, text=text, anchor="w")
        #     label.pack(fill="x")

        # 既存データをすべて削除
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        #2 カラムの設定             
        columns = ["要素名","型"]
            
        self.treeview['columns'] = columns
        # ID列を表示しない設定
        self.treeview['show'] = 'headings'  

        # 列の見出し(ヘッダー)を設定
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor='w')   #anchor='w'で左寄せ
            
        #データの挿入 (parent="", index="end")
        for col in structure:
                # 辞書型(values)をリスト変換して渡す
                # values = [r.get(col, "-") for col in columns] r.get(col)で取得できなかった時"-"を入れるという処理⇒失敗
            text = f""
            values = [col['name'], col['type']]
            self.treeview.insert("", "end", values=list(values))


    def show_data(self):
        state = self.controller.state_map
        data = state['query_result']
        structure =state['table_structure']

        # textboxへの処理はコメントアウト        
        # 見出し
        # header = ctk.CTkLabel(self.table_list, text=f"---  {state['selected_table']}  ---", anchor="w")
        # header.pack(fill="x")

        # # # column取得
        # colomns = data[0].keys()
        # # print("カラム:",colomns)

        # # # ヘッダ
        # header = ctk.CTkLabel(self.table_list, text="|".join(colomns),anchor="w")
        # header.pack(fill="x")

        # # スクロールラベルバーにボタンを追加
        # for row in data:
        #     values = [str(row[col]) for col in colomns]
        #     label = ctk.CTkLabel(self.table_list, text="|".join(values), anchor="w")
        #     label.pack(fill="x")                   
        
        # 既存データをすべて削除
        for item in self.treeview2.get_children():
            self.treeview2.delete(item)

        # カラム行だけでも作成して欲しいので、dataがなくても終了させない
        # if not data:
        #     return

        # カラムの設定
        # INSERTされたデータがないい場合でもカラムを作成したいため、テーブル構造からカラムを作成する              
        # columns = data[0].keys()
        columns = []
        for col in structure:
            columns.append(col['name'])
            
        self.treeview2['columns'] = list(columns)
        # ID列を表示しない設定
        self.treeview2['show'] = 'headings'  

        # 列の見出し(ヘッダー)を設定
        for col in columns:
            self.treeview2.heading(col, text=col)
            self.treeview2.column(col, width=100, anchor='w')   #anchor='w'で左寄せ
            
        #データの挿入 (parent="", index="end")
        for row in data:
            # 辞書型(values)をリスト変換して渡す
            values = [str(row[col]) for col in columns]
            self.treeview2.insert("", "end", values=list(values))

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = DB_ViewerApp()
    #イベント待ちループ開始
    app.mainloop()
