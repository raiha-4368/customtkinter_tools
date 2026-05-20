from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import json

class JsonViewerApp(ctk.CTkFrame):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="JsonVirere")
        label.pack()

        # -------------------------
        # menu_frame
        # -------------------------
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack()
        # -------------------------
        # menu_frame内の要素
        # ------------------------- 
        self.dir_select = ctk.CTkButton(self.menu_frame, text="ファイルを選択",command=self.select_json)
        self.dir_select.pack(side="left", pady=(10,10), padx=(10,10))

        self.clear_button = ctk.CTkButton(self.menu_frame, text="クリア",command=self.clear)
        self.clear_button.pack(side="left", pady=(10,10), padx=(10,10))


        # -------------------------
        # content_frame
        # -------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True,fill="both")
        # -------------------------
        # content_frame内の要素
        # -------------------------
        self.content_label = ctk.CTkLabel(self.content_frame, text="jsonファイルの中身を表示します")
        self.content_label.pack(pady=(30,10))

        self.path_label = ctk.CTkLabel(self.content_frame, text="path : ")
        self.path_label.pack(pady=(10,20))

        self.treeview = ttk.Treeview(self.content_frame)
        self.treeview.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))
        # 見出し設定
        self.treeview.heading("#0", text=f"jsonファイルビュー")

    #jsonファイル選択
    def select_json(self):
        try:
            filepath = dialogs.select_file(filetypes=[("json files", "*.json")],title="jsonファイルを選択")

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
