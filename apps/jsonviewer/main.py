import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import json

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JsonViewerApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("JsonViewer App")
        self.geometry("1200x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.side_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF")
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
        self.dir_select = ctk.CTkButton(self.side_frame, text="ファイルを選択",command=self.select_json)
        self.dir_select.pack(pady=(10,10), padx=(10,10))

        self.clear_button = ctk.CTkButton(self.side_frame, text="クリア",command=self.clear)
        self.clear_button.pack(pady=(10,10), padx=(10,10))

        # サイドメニューの下部にモードチェンジ用セグメントボタンを配置
        segemented_button = ctk.CTkSegmentedButton(self.side_frame, values=["System", "Dark", "Light"],
                                                     command=self.change_mode,
                                                     selected_color=("orange", "purple"),
                                                     selected_hover_color=("darkorange","indigo"))
        segemented_button.set(ctk.get_appearance_mode())    # 初期値を現在のモードに設定
        segemented_button.pack(side="bottom",pady=(10,10))


        # -------------------------
        # content_frame内の要素
        # -------------------------
        self.content_label = ctk.CTkLabel(self.content_frame,text="jsonファイルの中身を表示します")
        self.content_label.pack(pady=(30,10))

        self.path_label = ctk.CTkLabel(self.content_frame,text="path : ")
        self.path_label.pack(pady=(10,20))


        self.treeview = ttk.Treeview(self.content_frame)
        self.treeview.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))
        # 見出し設定
        self.treeview.heading("#0", text=f"jsonファイルビュー")



    #jsonファイル選択
    def select_json(self):
        try:
            filepath = dialogs.select_file(title="jsonファイルを選択")

            if filepath:
            
                p = Path(filepath)
                # パス表示のラベルを更新
                self.path_label.configure(text=f"path : {filepath}")

                #拡張子がjsonなら処理を実行
                if p.suffix == ".json":
                    # 既存データをすべて削除
                    for item in self.treeview.get_children():
                        self.treeview.delete(item)

                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                
                    # 親ノードの設定
                    current_node = self.treeview.insert("", "end", text="JSON", open=True)

                    self.explore_json(data, parent=current_node)
                else:
                    messagebox.showerror("エラー", "jsonファイルではありません。")
        
        except Exception as e:
            messagebox.showerror("エラー","jsonの構文が正しくありません")

    # jsonの中身を再帰的に見る処理
    def explore_json(self, data, parent=""):

        # 辞書(キーと値のペア)の場合
        if isinstance(data, dict):
            # 親ノード設定
            p = self.treeview.insert(parent, "end", text=f"[Dict of {len(data)} items]{{}}", open=True)
            for key, value in data.items():
                # 親ノード設定
                p2 = self.treeview.insert(p, "end", text=f"[Key:{key}]", open=True)
                self.explore_json(value, p2)

        # リスト(配列の場合)
        elif isinstance(data, list):
            # 親ノード設定
            p = self.treeview.insert(parent, "end", text=f"[List of {len(data)} items][]", open=True)
            for item in data:
                self.explore_json(item, p)

        # それ以外の場合
        else:
            self.treeview.insert(parent, "end", text=f"value: {data}")            


# クリア処理
    def clear(self):
        self.path_label.configure(text=f"path : ")
        # 既存データをすべて削除
        for item in self.treeview.get_children():
            self.treeview.delete(item)


    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = JsonViewerApp()
    #イベント待ちループ開始
    app.mainloop()

