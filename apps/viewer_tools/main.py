import tkinter as tk
import customtkinter as ctk

from apps.viewer_tools.regex import RegexApp
from apps.viewer_tools.xml_viewer import XmlViewerApp
from apps.viewer_tools.json_viewer import JsonViewerApp
from apps.viewer_tools.csv_viewer import CsvViewerApp
from apps.viewer_tools.diff import DifffilesApp
from apps.viewer_tools.treeviewer import TreeCommandApp
from apps.viewer_tools.db_viewer import DBViewerApp


# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# ======================================================================================================================

class NavigationFrame(ctk.CTkFrame):
    """サイドメニュー用のクラス"""
    def __init__(self, master, select_page_callback, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)

        self.grid_rowconfigure(10, weight=1) # 下部に余白を作る設定

        # タイトルラベル
        self.label = ctk.CTkLabel(self, text="Viewer Tools")
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # 切り替えボタン
        self.btn_page1 = ctk.CTkButton(self, text="TreeViewer", command=lambda: select_page_callback("TreeViewer"))
        
        self.btn_page1.grid(row=1, column=0, padx=20, pady=20)

        self.btn_page2 = ctk.CTkButton(self, text="Regex", command=lambda: select_page_callback("Regex"))
        self.btn_page2.grid(row=2, column=0, padx=20, pady=20)

        self.btn_page3 = ctk.CTkButton(self, text="Xml", command=lambda: select_page_callback("XmlViewer"))
        self.btn_page3.grid(row=3, column=0, padx=20, pady=20)
        
        self.btn_page4 = ctk.CTkButton(self, text="Csv", command=lambda: select_page_callback("CsvViewer"))
        self.btn_page4.grid(row=4, column=0, padx=20, pady=20)

        self.btn_page5 = ctk.CTkButton(self, text="Json", command=lambda: select_page_callback("JsonViewer"))
        self.btn_page5.grid(row=5, column=0, padx=20, pady=20)


        self.btn_page6 = ctk.CTkButton(self, text="Diff", command=lambda: select_page_callback("Diff"))
        self.btn_page6.grid(row=6, column=0, padx=20, pady=20)

        self.btn_page7 = ctk.CTkButton(self, text="DB", command=lambda: select_page_callback("DBViewer"))
        self.btn_page7.grid(row=7, column=0, padx=20, pady=20)

        # サイドメニューの下部にモードチェンジ用セグメントボタンを配置
        segemented_button = ctk.CTkSegmentedButton(self, values=["System", "Dark", "Light"],
                                                     command=self.change_mode,
                                                     selected_color=("orange", "purple"),
                                                     selected_hover_color=("darkorange","indigo"))
        segemented_button.set(ctk.get_appearance_mode())    # 初期値を現在のモードに設定
        segemented_button.grid(row=10, pady=(0,10))

    # TODO : 取り合えず実装見送り
    # def toggle_buttons(self, state):
    #     #ボタンの切り替え

    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)
# ======================================================================================================================

# ======================================================================================================================
class ViewerTools(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Timers App")
        self.geometry("1500x1000")

        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)


        # レイアウト設定(左:サイドメニュー、右:メインコンテンツ)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0, weight=1)

        # サイドメニューの配置
        self.navigation_frame = NavigationFrame(self, self.select_frame, width=140)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # 画面インスタンスの生成
        self.pages ={
            "TreeViewer" : TreeCommandApp(self, fg_color="transparent"),
            "Regex" : RegexApp(self, fg_color="transparent"),
            "XmlViewer" : XmlViewerApp(self, fg_color="transparent"),
            "CsvViewer" : CsvViewerApp(self, fg_color="transparent"),
            "JsonViewer" : JsonViewerApp(self, fg_color="transparent"),
            "Diff" : DifffilesApp(self, fg_color="transparent"),
            "DBViewer" : DBViewerApp(self, fg_color="transparent"),
            }

        # 初期表示
        self.select_frame("Countdown")

    def select_frame(self, name):
        """指定された名前のframeを表示し、他を隠す"""
        for page_name, page_instance in self.pages.items():
            if page_name == name:
                page_instance.grid(row=0, column=1, sticky="nsew")
            else:
                page_instance.grid_forget()

# ======================================================================================================================

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = ViewerTools()
    #イベント待ちループ開始
    app.mainloop()
