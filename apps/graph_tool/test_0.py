import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# テーマ設定（ダークモード）
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdvancedGraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CSV/Excel Analyzer Pro")
        self.geometry("1100x700")

        self.df = None
        self.canvas = None
        self.scroll_frame = None

        # ×ボタン終了時実行
        # self.protocol()はウィンドウマネージャ(OSのウィンドウシステム)から特定の操作(イベント)
        # とpythonの関数を紐づけるためのメソッド
        # WM_DELETE_WINDOWで×ボタン押下時の挙動を設定
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- レイアウト設定 ---
        # ウィンドウやフレームのサイズが変更されたときに
        # 中のパーツ(ウィジェット)をどのように自動で拡大・縮小させるかを指定する設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
        
        # ==========================================
        # 🟢 左側：共通操作パネル
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.btn_import = ctk.CTkButton(self.sidebar, text="📁 ファイル読み込み", command=self.import_file, height=40)
        self.btn_import.pack(pady=20, padx=15, fill="x")

        self.set_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        # ==========================================
        # 🔵 右側：画面切り替え（タブコントロール）
        # ==========================================
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.tab_graph = self.tab_view.add("📊 グラフ表示")
        self.tab_viewer = self.tab_view.add("📋 データビューア")

        # 2. MatplotlibのFigure（土台）とAxes（描画領域）を作成
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # 3. FigureをTkinterで使えるキャンバスに変換して配置
        canvas = FigureCanvasTkAgg(fig, master=self.tab_graph)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def import_file(self):

        return


    def on_closing(self):
        print("終了")
        plt.close('all')
        for child in self.winfo_children():
            child.destroy()
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = AdvancedGraphApp()
    app.mainloop()
