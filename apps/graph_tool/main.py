import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs,files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import japanize_matplotlib      # グラフ内の日本語文字表示用ライブラリ。インポートしないと日本語が文字化けする

import numpy as np

import matplotlib.pyplot as plt


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
        self.side_frame.grid_rowconfigure(10, weight=1)

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
        self.records = []
        self.data_list = []
        self.key_list = []
        self.vertical_list = []
        self.graph_type = ""

        # -------------------------
        # side_frame内の要素
        # -------------------------
        label0 = ctk.CTkLabel(self.side_frame, text="グラフ選択")
        label0.grid(row=1, pady=(10,10), padx=(10,10))

        self.graph_conbobox = ctk.CTkComboBox(self.side_frame, values=["折れ線グラフ", "散布図","円グラフ","ヒストグラム"], command=self.graph_chenge, state="readonly")
        self.graph_conbobox.grid(row=2, pady=(10,10), padx=(10,10))
        self.graph_conbobox.set("折れ線グラフ")

        label = ctk.CTkLabel(self.side_frame, text="x(横)軸選択\n※x軸は文字列として扱う")
        label.grid(row=3, pady=(10,10), padx=(10,10))

        # x(横)軸
        self.x_axis_conbobox = ctk.CTkComboBox(self.side_frame, values=["未設定"], command=None, state="readonly")
        self.x_axis_conbobox.grid(row=4, pady=(10,10), padx=(10,10))
        self.x_axis_conbobox.set("未設定")

        label2 = ctk.CTkLabel(self.side_frame, text="y(縦)軸選択\ny軸は数値のみを扱う")
        label2.grid(row=5, pady=(10,10), padx=(10,10))

        # y(縦)軸
        self.y_axis_conbobox = ctk.CTkComboBox(self.side_frame, values=["未設定"], command=None, state="readonly")
        self.y_axis_conbobox.grid(row=6, pady=(10,10), padx=(10,10))
        self.y_axis_conbobox.set("未設定")

        self.dir_select = ctk.CTkButton(self.side_frame, text="ファイルを選択",command=self.import_file)
        self.dir_select.grid(row=7, pady=(10,10), padx=(10,10))

        self.graph_button = ctk.CTkButton(self.side_frame, text="グラフ描画",command=self.display_graph)
        self.graph_button.grid(row=8, pady=(10,10), padx=(10,10))

        # サイドメニューの下部にモードチェンジ用セグメントボタンを配置
        segemented_button = ctk.CTkSegmentedButton(self.side_frame, values=["System", "Dark", "Light"],
                                                     command=self.change_mode,
                                                     selected_color=("orange", "purple"),
                                                     selected_hover_color=("darkorange","indigo"))
        segemented_button.set(ctk.get_appearance_mode())    # 初期値を現在のモードに設定
        segemented_button.grid(row=15, pady=(0,10))

        # -------------------------
        # content_frame内の要素
        # -------------------------
        # タブ設定
        self.tab = ctk.CTkTabview(self.content_frame)
        self.tab.pack(fill=tk.BOTH, expand=True)

        self.tab_data = self.tab.add("データ")
        self.tab_graph = self.tab.add("グラフ")

        # グラフ描画
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.label1 = ctk.CTkLabel(self.tab_graph, text="")
        self.label1.pack()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # データタブ
        self.treeview = ttk.Treeview(self.tab_data)
        self.treeview.pack(fill=ctk.BOTH, expand=True)
        # スクロールバー設定
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def axis_choice(self):
        self.x_axis = self.x_axis_conbobox.get()
        self.y_axis = self.y_axis_conbobox.get()

    def set_axis_conbobox(self):
        
        values = ["未設定"]
        values.extend(self.vertical_list.keys())
        self.x_axis_conbobox.configure(values=values)
        self.y_axis_conbobox.configure(values=values)


    # グラフ選択コンボボックス選択時
    def graph_chenge(self, choice):
        self.display_graph()

    # グラフ描画処理
    def display_graph(self):
        print("グラフ描画")

        try:
            
            # 現在のコンボボックスの選択を取得
            self.graph_type = self.graph_conbobox.get()
            if not self.graph_type:
                messagebox.showerror("エラー","グラフが選択されていません。")
                return

            print(f"グラフタイプ:{self.graph_type}")
            self.axis_choice()

            # 軸設定を取得
            print(f"x軸:{self.x_axis}")
            print(f"y軸:{self.y_axis}")
            if self.y_axis == "未設定":
                messagebox.showerror("エラー", "y軸を選択してください")



            # グラフ設定
            # グラフのclear処理
            self.ax.clear()

            # 円グラフ処理を実行するとグラフのアスペクト比が縦長に変更されてしまう
            # そのため、ここでそのアスペクト比を初期化する
            self.ax.set_aspect("auto", adjustable="datalim")
            x_data = []
            y_data = []
            print(f"key_list:{self.key_list}")
            for key in self.vertical_list:
                # x軸設定の一致を確認
                if key == self.x_axis:
                    x_data = self.vertical_list[key]
                if key == self.y_axis:
                    y_data =[int(x) for x in self.vertical_list[key]] 

            if self.graph_type == "折れ線グラフ":                
                self.label1.configure(text="y軸の設定を折れ線グラフで表示します。")

                if x_data and y_data:
                    self.ax.plot(x_data, y_data, label=f"{x_data}")
                    self.ax.set_title(f"Display: 折れ線グラフ\npaht :{self.filepath}")
                    # 凡例表示
                    self.ax.legend()

            # ヒストグラムは数値とした扱うy軸のみを使う
            elif self.graph_type ==  "ヒストグラム":
                self.label1.configure(text="y軸の設定をヒストグラムで表示します。")
                # サンプルデータ
                # data = np.random.normal(loc=50, scale=10, size=100)

                # ヒストグラム描画
                self.ax.hist(y_data,bins=20, label=f"{y_data}")
                self.ax.set_title(f"Display: ヒストグラム\npaht :{self.filepath}")
                # 凡例表示
                self.ax.legend()

            elif self.graph_type == "散布図":
                self.label1.configure(text="y軸の設定を散布図で表示します。")

                self.ax.scatter(x_data, y_data, label=f"")
                self.ax.set_title(f"Display: 散布図\npaht :{self.filepath}")
                # 凡例表示
                self.ax.legend()
            elif self.graph_type == "円グラフ":
                self.label1.configure(text="y軸の設定を円グラフで表示します。")
                # autopct="%1.1f%%で パーセントを自動計算し表示
                # もし、パーセントだけでなく実際の数値も表示したい場合は自分で計算処理を入れる必要がある
                self.ax.pie(y_data,labels=y_data, autopct="%1.1f%%")
                self.ax.set_title(f"Display: 円グラフ\npaht :{self.filepath}")
                # 円グラフでは凡例を表示しない

            else:
                pass

            if self.graph_type:
                # キャンバスの更新
                self.canvas.draw()

        except Exception as e:
            messagebox.showerror("エラー","y軸に文字列を含めることは出来ません。")
      

    def import_file(self):

        self.filepath = dialogs.select_file(
                title="csvファイルを選択してください", 
                filetypes=[(("csv Files","*.csv"))])
        if self.filepath:
            # 初期化
            # カラム行
            self.key_list = []
            # 縦一列
            self.vertical_list = {}


            # commonでの読み込み
            self.records, self.key_list = files.read_csv_file(self.filepath)


            print("縦列設定")
            for key in self.key_list:
                tate_list = []
                for row in self.records:
                    print(f"key:{key}")
                    print(f"取得:{row}")
                    print(f"key取得:{row[key]}")
                    tate_list.append(row[key])
                print("縦格納")
                print(tate_list)
                self.vertical_list[key] = tate_list

            print("最終取り出し")
            for r in self.vertical_list:
                print(self.vertical_list[r])

            # データタブ用のツリービュー表示            
            #1 既存データをすべて削除
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            #2 カラムの設定             
            # 以下でlist化する時、カラム行より多い要素があるとき、その列をNoneとして格納してしまう
            # columns = list(record[0].keys())
            # colがNoneの時はcolumnsに含めないよう以下とする
            columns = [col for col in self.records[0].keys() if col]
            
            #もしkeysにNoneを含んでいるのならflagをTrueとし、警告メッセージを表示する
            worning_flag = False
            for c in list(self.records[0].keys()):
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
            for r in self.records:
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
            
            self.set_axis_conbobox()
            self.display_graph()


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
