import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
# import japanize_matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# 独自のテーマとカラー（ダークモード）
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GraphApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CSV Graph Viewer")
        self.geometry("900x600")

        # 👇【追加1】×ボタンが押された時のカスタム処理を登録
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # データの保持用変数
        self.df = None

        # --- レイアウト設定（左右分割） ---
        self.grid_columnconfigure(0, weight=1)  # 左側：操作パネル
        self.grid_columnconfigure(1, weight=4)  # 右側：グラフ表示エリア
        self.grid_rowconfigure(0, weight=1)

        # *************************************************************************
        # --- 左側：操作パネル ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # ファイル選択ボタン
        self.btn_import = ctk.CTkButton(
            self.sidebar, text="CSV / Excel 読み込み", command=self.import_file
        )
        self.btn_import.pack(pady=20, padx=10, fill="x")

        # X軸選択ラベルとコンボボックス
        self.lbl_x = ctk.CTkLabel(
            self.sidebar, text="X軸（横軸）にする列:", anchor="w"
        )
        self.lbl_x.pack(pady=(10, 0), padx=10, fill="x")
        self.combo_x = ctk.CTkComboBox(self.sidebar, values=["ファイルを選択してください"])
        self.combo_x.pack(pady=5, padx=10, fill="x")

        # Y軸選択ラベルとコンボボックス
        self.lbl_y = ctk.CTkLabel(
            self.sidebar, text="Y軸（縦軸）にする列:", anchor="w"
        )
        self.lbl_y.pack(pady=(10, 0), padx=10, fill="x")
        self.combo_y = ctk.CTkComboBox(self.sidebar, values=["ファイルを選択してください"])
        self.combo_y.pack(pady=5, padx=10, fill="x")

        # グラフ描画ボタン
        self.btn_plot = ctk.CTkButton(
            self.sidebar, text="グラフを描画", command=self.draw_graph, state="disabled"
        )
        self.btn_plot.pack(pady=30, padx=10, fill="x")

        self.var = ctk.StringVar(value="折れ線")
        modes = ["折れ線", "散布図", "棒グラフ"]
        for i, text in enumerate(modes):
            radio = ctk.CTkRadioButton(self.sidebar, text=text, variable=self.var, value=text, 
                   command=self.update_graph)
            radio.pack(pady=10,padx=10)
            # radio.place(relx=0.38 + (i * 0.12), rely=0.55, anchor="center")        
        
        # *************************************************************************

        # *************************************************************************
        # --- 右側：グラフ表示エリア ---
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 初期状態のメッセージ
        self.lbl_status = ctk.CTkLabel(
            self.graph_frame, text="ファイルを開いて、軸を選択してください"
        )
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")
        

        # グラフを埋め込むためのキャンバス変数
        self.canvas = None



        # *************************************************************************

    def import_file(self):
        """ファイルを読み込んでコンボボックスの選択肢を更新する"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("データファイル", "*.csv *.xlsx *.xls"),
                ("CSVファイル", "*.csv"),
                ("Excelファイル", "*.xlsx *.xls"),
            ]
        )

        if not file_path:
            return

        # 拡張子に合わせてPandasで読み込み
        _, ext = os.path.splitext(file_path)
        try:
            if ext.lower() == ".csv":
                self.df = pd.read_csv(file_path)
            else:
                self.df = pd.read_excel(file_path)

            # CSVの列名（カラム）をリストで取得
            columns = list(self.df.columns)

            # コンボボックスの選択肢を、取得した列名に更新
            self.combo_x.configure(values=columns)
            self.combo_y.configure(values=columns)

            # 初期値をセット（1番目と2番目の列）
            self.combo_x.set(columns[0])
            if len(columns) > 1:
                self.combo_y.set(columns[1])
            else:
                self.combo_y.set(columns[0])

            # ボタンを有効化
            self.btn_plot.configure(state="normal")
            self.lbl_status.configure(text=f"読み込み完了: {os.path.basename(file_path)}")

        except Exception as e:
            self.lbl_status.configure(text=f"エラーが発生しました:\n{str(e)}")

    def draw_graph(self):
        """選択された軸を元にMatplotlibグラフを画面内に描画する"""
        if self.df is None:
            return

        # コンボボックスから現在選択されている列名を取得
        x_col = self.combo_x.get()
        y_col = self.combo_y.get()

        # 以前のグラフが残っていれば削除してクリア
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.lbl_status.place_forget()  # 初期メッセージを非表示に

        # --- Matplotlibでグラフを作成 ---
        # 画面のテーマに合わせて背景色を設定 (CustomTkinterのダークグレー #2b2b2b に合わせる)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        # データの描画
        ax.plot(
            self.df[x_col],
            self.df[y_col],
            marker="o",
            color="#1f77b4",
            linewidth=2,
        )

        # 見栄えの設定（文字色を白にする）
        ax.set_title(f"{y_col} の推移", color="white", fontsize=14, pad=15)
        ax.set_xlabel(x_col, color="white", fontsize=12)
        ax.set_ylabel(y_col, color="white", fontsize=12)
        ax.tick_params(colors="white")  # 目盛りの色
        ax.grid(True, linestyle="--", alpha=0.5)

        # 枠線の色を薄くする
        for spine in ax.spines.values():
            spine.set_color("#444444")

        # グラフを整える
        fig.tight_layout()

        # --- CustomTkinterの画面にグラフを埋め込む ---
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_graph(self):
        """選択されたグラフの種類に合わせて再描画する関数"""
        # データの準備
        # x = np.linspace(0, 10, 50)
        x = None
        y = None
        graph_type = self.var.get()
    
        # 以前のグラフが残っていれば削除してクリア
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

    
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        # 種類の切り替え
        if graph_type == "折れ線":
            ax.plot(x, y, label="Sin Wave", color="blue")
        elif graph_type == "散布図":
            ax.scatter(x, y, label="Scatter Points", color="red")
        elif graph_type == "棒グラフ":
            ax.bar(["A", "B", "C", "D"], [5, 20, 15, 25], color="green")
    
        ax.set_title(f"Display: {graph_type}")
        ax.legend()
    
        # キャンバスの更新
        self.canvas.draw()

    # 👇【追加2】クラスの一番下などに、この終了処理メソッドを足してください
    def on_closing(self):
        """ウインドウを閉じる前に子要素をすべて削除して安全に終了する"""
        # Matplotlibのグラフが開いている場合はメモリを解放
        if hasattr(self, 'canvas') and self.canvas:
            plt.close('all')
        
        # 自クラスの子要素（ウィジェット）を全て明示的に破棄
        for child in self.winfo_children():
            child.destroy()
            
        # 最後にアプリ本体を終了
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
