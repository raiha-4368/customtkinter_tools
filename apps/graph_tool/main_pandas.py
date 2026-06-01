import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs,files
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import japanize_matplotlib


# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GraphApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("GraphApp")
        self.geometry("1200x800")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.side_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.side_frame.pack(side=ctk.LEFT, fill=ctk.Y)

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH)

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
        file_menu.add_command(label="終了", command=self.quit)

        # -------------------------
        # 変数宣言
        # -------------------------

        # -------------------------
        # side_frame内の要素
        # -------------------------
        self.dir_select = ctk.CTkButton(self.side_frame, text="ファイルを選択",command=self.import_file)
        self.dir_select.pack(pady=(10,10), padx=(10,10))



        # -------------------------
        # content_frame内の要素
        # -------------------------
        # タブ設定
        self.tab = ctk.CTkTabview(self.content_frame)
        self.tab.pack(fill=tk.BOTH, expand=True)

        self.tab_graph = self.tab.add("グラフ")
        self.tab_data = self.tab.add("データ")

        # グラフ描画
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # データタブ
        self.treeview = ttk.Treeview(self.tab_data)
        self.treeview.pack(fill=ctk.BOTH, expand=True)
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)



    def import_file(self):

        data_list = []
        key_list = []

        filepath = dialogs.select_file(
                title="csvファイルを選択してください", 
                filetypes=[(("csv Files","*.csv"))])
        if filepath:
            # 確認用
            print(filepath)

            # pandasでの読み込み
            self.df = pd.read_csv(filepath)

            # commonでの読み込み
            records = files.read_csv_file(filepath)

            for row in records:
                print(row)

                # 回数も数えてる(一応)
                for i, key in enumerate(row, start=1):
                    print(row[key])
                    key_list.append(key)
                    data_list.append(row[key])
            print(data_list)

            # pandasの戻り値df(データフレーム)の確認
            print("***********************")
            print(self.df)

            print("***********************")
            for r in self.df:
                print(r)
            # 先頭5行
            print(self.df.head())
            print(self.df.tail())
            print(self.df.info())
            print(self.df.shape)

            print("***********************")
            print("1列目")
            print(self.df.iloc[:, 0])
            print("***********************")

            print("***********************")
            print("カラム")
            print(self.df.columns)
            for c in self.df.columns:
                print(c)
            print("***********************")


            # グラフ設定
            # 折れ線

            # グラフのclear処理
            self.ax.clear()

            self.ax.plot(key_list, data_list, label="csv data")

            self.ax.set_title(f"Display: 折れ線グラフ")
            self.ax.legend()

            # キャンバスの更新
            self.canvas.draw()
            
            #1 既存データをすべて削除
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            #2 カラムの設定             
            # 以下でlist化する時、カラム行より多い要素があるとき、その列をNoneとして格納してしまう
            # columns = list(record[0].keys())
            # colがNoneの時はcolumnsに含めないよう以下とする
            columns = [col for col in records[0].keys() if col]
            
            #もしkeysにNoneを含んでいるのならflagをTrueとし、警告メッセージを表示する
            worning_flag = False
            for c in list(records[0].keys()):
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
            for r in records:
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





    # ×ボタン押下による終了時にグラフ描画処理が残ってしまうのでここで終了させる
    def on_closing(self):
        # plt,close('all')

        self.quit()
        self.destroy()

    
		# モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = GraphApp()
    #イベント待ちループ開始
    app.mainloop()
