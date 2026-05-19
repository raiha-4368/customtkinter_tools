import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import xml.etree.ElementTree as ET

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class XmlViewerApp(ctk.CTkFrame):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="XmlVirere")
        label.pack()

        # -------------------------
        # side_frame内の要素
        # -------------------------
        self.dir_select = ctk.CTkButton(self, text="ファイルを選択",command=self.select_xml)
        self.dir_select.pack(pady=(10,10), padx=(10,10))

        self.clear_button = ctk.CTkButton(self, text="クリア",command=self.clear)
        self.clear_button.pack(pady=(10,10), padx=(10,10))

        # -------------------------
        # content_frame内の要素
        # -------------------------
        self.content_label = ctk.CTkLabel(self,text="xmlファイルの中身を表示します")
        self.content_label.pack(pady=(30,10))

        self.path_label = ctk.CTkLabel(self,text="path : ")
        self.path_label.pack(pady=(10,20))


        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))
        # 見出し設定
        self.treeview.heading("#0", text=f"xmlファイルビュー")



    #jsonファイル選択
    def select_xml(self):

        try:
            filepath = dialogs.select_file(title="xmlファイルを選択")

            if filepath:
            
                p = Path(filepath)
                # パス表示のラベルを更新
                self.path_label.configure(text=f"path : {filepath}")

                #拡張子がjsonなら処理を実行
                if p.suffix == ".xml":
                    # 既存データをすべて削除
                    self.treeview.delete(*self.treeview.get_children())
    
                    xml_tree = ET.parse(filepath)
                    xml_root = xml_tree.getroot()

                    self.add_xml_to_tree("", xml_root)
                else:
                    messagebox.showerror("エラー", "xmlファイルではありません。")
        except Exception as e:
            messagebox.showerror("エラー", "xmlの構文が正しくありません")

    #xmlの読み込み再帰処理
    def add_xml_to_tree(self, parent_node, element):
        """
        XMLの要素を再帰的にTreeviewに追加する
        """
        has_child = len(element) > 0
        # 絵文字を接頭辞として使う
        prefix = "📂 " if has_child else "📄 "
    
        display_text = f"{prefix}{element.tag}"
        if element.attrib:
            display_text += f"{element.attrib}"

        content = element.text.strip() if element.text else ""
        if content:
            display_text += f" : {content}"

        current_node = self.treeview.insert(parent_node, "end", text=display_text, open=True)

        for child in element:
            self.add_xml_to_tree(current_node, child)
  


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
    app = XmlViewerApp()
    #イベント待ちループ開始
    app.mainloop()

