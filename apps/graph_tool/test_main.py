import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# テーマ設定（ダークモード）
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 日本語フォント設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Hiragino Maru Gothic Pro', 'AppleGothic', 'sans-serif']

class AdvancedGraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CSV/Excel Analyzer Pro")
        self.geometry("1100x700")

        self.df = None
        self.canvas = None
        self.scroll_frame = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- レイアウト設定 ---
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
        
        # 💡 データ形式の選択を追加
        ctk.CTkLabel(self.set_frame, text="データの並び方:", anchor="w").pack(pady=(10, 0), padx=15, fill="x")
        self.data_mode = ctk.StringVar(value="通常のデータ（縦長）")
        self.combo_mode = ctk.CTkComboBox(
            self.set_frame, 
            values=["通常のデータ（縦長）", "1行のデータを列ごとに並べる（横長）"],
            variable=self.data_mode,
            command=self.change_data_mode
        )
        self.combo_mode.pack(pady=5, padx=15, fill="x")

        # 軸選択エリアの親枠
        self.axis_select_frame = ctk.CTkFrame(self.set_frame, fg_color="transparent")
        self.axis_select_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(self.axis_select_frame, text="X軸（項目・横軸）:", anchor="w").pack(pady=(10, 0), padx=15, fill="x")
        self.combo_x = ctk.CTkComboBox(self.axis_select_frame, values=[])
        self.combo_x.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.axis_select_frame, text="Y軸（数値・縦軸）:", anchor="w").pack(pady=(10, 0), padx=15, fill="x")
        self.combo_y = ctk.CTkComboBox(self.axis_select_frame, values=[])
        self.combo_y.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.set_frame, text="グラフの種類:", anchor="w").pack(pady=(15, 0), padx=15, fill="x")
        self.graph_type = ctk.StringVar(value="棒グラフ")  # 初期値を棒グラフに変更
        for t in ["折れ線", "棒グラフ", "円グラフ"]:
            r = ctk.CTkRadioButton(self.set_frame, text=t, variable=self.graph_type, value=t)
            r.pack(pady=5, padx=25, anchor="w")

        self.btn_plot = ctk.CTkButton(self.set_frame, text="📊 グラフを描画", command=self.draw_graph, fg_color="#2c3e50", hover_color="#34495e")
        self.btn_plot.pack(pady=25, padx=15, fill="x")

        # ==========================================
        # 🔵 右側：画面切り替え（タブコントロール）
        # ==========================================
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.tab_graph = self.tab_view.add("📊 グラフ表示")
        self.tab_viewer = self.tab_view.add("📋 データビューア")

        self.lbl_status = ctk.CTkLabel(self.tab_graph, text="ファイルを読み込んでください", font=("", 16))
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")

        self.viewer_text = tk.Text(self.tab_viewer, bg="#2b2b2b", fg="white", wrap="none", font=("Courier", 10))
        self.viewer_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.viewer_text.config(state="disabled")

    def import_file(self):
        """ファイルを読み込み、ビューアを更新"""
        file_path = filedialog.askopenfilename(filetypes=[("データファイル", "*.csv *.xlsx *.xls")])
        if not file_path:
            return

        _, ext = os.path.splitext(file_path)
        try:
            if ext.lower() == ".csv":
                self.df_original = pd.read_csv(file_path)
            else:
                self.df_original = pd.read_excel(file_path)

            # 初期状態は「通常のデータ」としてセット
            self.combo_mode.set("通常のデータ（縦長）")
            self.update_data_processing()

            self.set_frame.pack(fill="both", expand=True)
            self.lbl_status.configure(text=f"読み込み完了: {os.path.basename(file_path)}\n「グラフを描画」を押してください")

            # ビューアの更新
            self.viewer_text.config(state="normal")
            self.viewer_text.delete("1.0", tk.END)
            self.viewer_text.insert("1.0", self.df_original.to_string(index=False))
            self.viewer_text.config(state="disabled")

        except Exception as e:
            self.lbl_status.configure(text=f"エラーが発生しました:\n{str(e)}")

    def change_data_mode(self, choice):
        """並び方コンボボックスが切り替わったときの処理"""
        if self.df_original is None:
            return
        self.update_data_processing()

    def update_data_processing(self):
        """選択されたモードに応じてデータを整形し、軸選択を更新"""
        mode = self.data_mode.get()
        
        if mode == "1行のデータを列ごとに並べる（横長）":
            # 💡 【魔法の処理】データを転置（縦横変換）する
            # a,b,c... の列名を「項目」という列のデータに変換します
            self.df = self.df_original.iloc[[0]].T.reset_index()
            self.df.columns = ["項目", "値"]
            
            # 横長モードのときは軸選択を固定（隠す）
            self.axis_select_frame.pack_forget()
        else:
            # 通常モード
            self.df = self.df_original.copy()
            columns = list(self.df.columns)
            self.combo_x.configure(values=columns)
            self.combo_y.configure(values=columns)
            self.combo_x.set(columns[0])
            self.combo_y.set(columns[1] if len(columns) > 1 else columns[0])
            self.axis_select_frame.pack(fill="x", pady=5)

    def draw_graph(self):
        """グラフを描画"""
        if self.df is None:
            return

        mode = self.data_mode.get()
        if mode == "1行のデータを列ごとに並べる（横長）":
            x_col = "項目"
            y_col = "値"
        else:
            x_col = self.combo_x.get()
            y_col = self.combo_y.get()
            
        g_type = self.graph_type.get()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.scroll_frame:
            self.scroll_frame.destroy()
        self.lbl_status.place_forget()

        try:
            data_count = len(self.df)

            # 横幅スクロールの判定
            if g_type in ["折れ線", "棒グラフ"] and data_count > 20:
                fig_width = 7 + (data_count - 20) * 0.3
                self.scroll_frame = ctk.CTkScrollableFrame(self.tab_graph, orientation="horizontal")
                self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
                master_frame = self.scroll_frame
            else:
                fig_width = 7
                master_frame = self.tab_graph

            fig, ax = plt.subplots(figsize=(fig_width, 5), facecolor="#2b2b2b")
            ax.set_facecolor("#2b2b2b")

            # 数値型に変換して描画
            y_data = pd.to_numeric(self.df[y_col], errors='coerce')

            if g_type == "折れ線":
                ax.plot(self.df[x_col].astype(str), y_data, marker="o", color="#3498db", linewidth=2)
                ax.grid(True, linestyle="--", alpha=0.3)
                plt.xticks(rotation=45, ha='right')
            elif g_type == "棒グラフ":
                # 💡 ここで a, b, c... が横一列の棒になります！
                ax.bar(self.df[x_col].astype(str), y_data, color="#2ecc71", alpha=0.8, width=0.5)
                ax.grid(True, linestyle="--", alpha=0.3, axis='y')
                plt.xticks(rotation=45, ha='right')
            elif g_type == "円グラフ":
                ax.pie(y_data.dropna(), labels=self.df[x_col][y_data.notna()], autopct='%1.1f%%', textprops={'color': 'white'}, startangle=90)
                ax.axis('equal')

            if g_type != "円グラフ":
                ax.set_title(f"データ一覧 ({g_type})", color="white", fontsize=14, pad=15)
                ax.tick_params(colors="white", labelsize=10)
                for spine in ax.spines.values():
                    spine.set_color("#444444")

            fig.tight_layout()

            self.canvas = FigureCanvasTkAgg(fig, master=master_frame)
            self.canvas.draw()
            
            if g_type in ["折れ線", "棒グラフ"] and data_count > 20:
                self.canvas.get_tk_widget().pack(fill="y", expand=True, width=int(fig_width * 95))
            else:
                self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            self.tab_view.set("📊 グラフ表示")

        except Exception as e:
            if self.scroll_frame:
                self.scroll_frame.destroy()
            self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")
            self.lbl_status.configure(text=f"描画エラー: データ内容を確認してください\n({str(e)})")

    def on_closing(self):
        plt.close('all')
        for child in self.winfo_children():
            child.destroy()
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = AdvancedGraphApp()
    app.mainloop()
