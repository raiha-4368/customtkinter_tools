import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MemoApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()
                
        self.configure(fg_color="#1a1a1a")
        self.title("Memo App *.txt")
        self.geometry("800x800")
        # -------------------------
        # ショートカット設定
        # Control-Shiftと順番が決まっている
        # 小文字のs(s)と大文字のS(Shift+s)の使い分け
        # -------------------------
        self.bind("<Control-s>", lambda e: self.update_file())
        self.bind("<Control-S>", lambda e: self.save_file())
        # mac用(動作未確認)
        # self.bind("<Command-Shift-s>", lambda e: self.save_file())

        # ×ボタンが押されたときに実行する関数を登録
        self.protocol("WM_DELETE_WINDOW", self.close_memo)

        # キー入力を監視
        self.bind("<Key>", self.monitoring_text)
        
        # 参考用
        # キーを離した瞬間にカウント関数を呼ぶ（KeyReleaseを使うのがコツ）
        # self.textbox.bind("<KeyRelease>", None)

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.main_frame.pack()

        #初期表示
        self.create_widgets()
    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_widgets(self):
        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="ファイルを開く", command=self.import_file)
        file_menu.add_separator()
        file_menu.add_command(label="名前を付けて保存/Ctrl+Shift+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="上書き保存/Ctrl+s", command=self.update_file)
        file_menu.add_separator()
        file_menu.add_command(label="クリア(読み込み状況/テキストボックス)", command=self.clear)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.close_memo)
        # 確認無しで終了する処理
        # file_menu.add_command(label="終了", command=self.quit)

        # テキストエリアの作成（幅と高さを指定可能）
        # expand=True, fill="both" でウィンドウサイズに追従
        self.textbox = ctk.CTkTextbox(self.main_frame,
                                        width=1000,
                                        height=740,
                                        fg_color="#ffffff",
                                        text_color="#000000",
                                        undo=True                   # undo=Trueを指定することでCtl+Zが自動で有効になります
                                        )
        self.textbox.pack(pady=(10,10),padx=(10,10),expand=True,fill="both")

        self.current_path = ""

        # テキストの文字数カウント
        self.text_count = 0
        # 保存確認フラグ
        self.save_flag = False

        # 状態表示用のラベル
        self.status_label = ctk.CTkLabel(self.main_frame, text="テキストは保存されていません")
        self.status_label.pack(side="left")
        self.text_count_label = ctk.CTkLabel(self.main_frame, text=f"入力:    {self.text_count}文字") 
        self.text_count_label.pack(side="right")


    def save_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension = ".txt",
            filetypes=[("text files", "*.txt")],
            title="textファイルを保存"
        )

        # print(self.textbox.get("1.0", "end"))

        if filepath:
            # "end-1c"で余計な改行を削除
            content = self.textbox.get("1.0", "end-1c")

        #新規書き込みw,追記モードaで使い分け
            with open(filepath, mode='w', newline="", encoding="utf-8") as f:
                f.write(content)

          # オプション 今開いているファイル名をタイトルに表示
            self.title(f"Memo App - {filepath}")
            self.current_path = filepath

            # 保存状況を反映
            self.status_label.configure(text="テキストは保存済みです")
            self.save_flag = True

            return True
        # filepathを持っていない=×等でファイアログをキャンセルしている
        else:
           return False

    def update_file(self):
       # selfがcurrent_pathを持っているなら処理
      if self.current_path:
        # フルパスからファイル名だけを抜き出す
        current_name = os.path.basename(self.current_path)

        # テキストエリアの記述内容を取得
        content = self.textbox.get("1.0", "end-1c")

        # ダイアログを表示⇒上書き表示の時はダイアログを表示しないよう変更
        # file_path = filedialog.asksaveasfilename(
        #    initialfile=current_name, #ここで既存ファイル名をダイアログ上に入れる
        #    defaultextension=".txt",
        #    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        #    title="名前を付けてを保存"
        # )

        # ダイアログ表示時は、ダイアログで選んだファイルパスを使用する
        # ダイアログ非表示なので、既存のファイルパスを使用する
        with open(self.current_path, mode='w', newline="", encoding="utf-8") as f:
          f.write(content)
        # 保存状況を反映
        self.status_label.configure(text="テキストは保存済みです")
        self.save_flag = True

      else:
          self.save_file()

    def import_file(self):

      filepath = filedialog.askopenfilename(
          defaultextension=".txt",
          filetypes=[("text files", "*.txt"), ("All files", "*.*")],
          title="ファイルを開く"
      )
      if filepath:
        try:
          with open(filepath, mode='r', encoding="utf-8") as f:
             content = f.read()
             # 確認用
            #  print(content)
          # テキストエリアを一度空にしてから読み込んだ内容を挿入
          self.textbox.delete("1.0", "end") #1行目から最後まで削除
          self.textbox.insert("1.0", content) #1行目に挿入

          # オプション 今開いているファイル名をタイトルに表示
          self.title(f"Memo App - {filepath}")

          # selfにファイルパスを持たせておく
          self.current_path = filepath

          # 保存状況を表示(開いたばかりのファイルなので保存済み扱いとする)
          self.status_label.configure(text="テキストは保存済みです")
          self.save_flag = True

          # 文字数をカウント
          self.textbox_count()

        except Exception as e:
           print(e)
           print("エラーが発生しました")

    # キー入力を監視→labelへtextboxの入力状況を反映
    def monitoring_text(self,event):
        # event.char : 押された文字 (a, b, c...)
        # event.keysym : キーの名前 (Return, Escape, space...)
        # print(f"押されたキー: {event.keysym}")
        # キーが入力されても文字数が変わらなければ保存ラベルの更新は行わない
        if not self.textbox_count():
            return
        # 保存状況を反映
        self.status_label.configure(text="テキストは保存されていません")
        self.save_flag = False

    # テキストボックスの文字数をカウント
    def textbox_count(self):
        before_text_count = self.text_count
        self.text_count = len(self.textbox.get("1.0", "end-1c"))
        self.text_count_label.configure(text=f"入力:    {self.text_count}文字")

        # キー入力でも文字数が変わらなかったらFalseを返却
        if before_text_count == self.text_count:
            return False
        return True
           
    # クリア機能
    def clear(self):
        # テキストボックスを1行目から最後まで削除
        self.textbox.delete("1.0", "end")

        # 保持しているファイルパスもクリア
        self.current_path = ""

        # タイトルも初期状態に戻す
        self.title("Memo App *.txt")

        # 保存状況もリセット
        self.status_label.configure(text="テキストは保存されていません")
        self.save_flag = False

        # テキストカウント再取得
        # 上記でクリアしているので0になる
        self.textbox_count()

    # 終了処理
    def close_memo(self):        
        should_close = True
        # テキストがあり、克テキストが保存されていない時、その趣旨を表示する
        if self.text_count > 0 and not self.save_flag:
            result = messagebox.askyesnocancel("終了の確認","テキストが保存されていません。\nウィンドウを閉じる前に保存しますか?")
            # キャンセルで終了しない
            if result is None:
                should_close = False
            # Yesで保存処理
            elif result:
                # current_pathがあるなら上書き
                if self.current_path != "":
                    self.update_file()
                else:
                    # ファイル保存ダイアログを×やキャンセルしたら終了しない
                    if not self.save_file():
                        should_close = False
        # 保存済みテキスト、テキスト無し、No選択、保存を行ったら終了
        if should_close:
            self.destroy()
           

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = MemoApp()
    #イベント待ちループ開始
    app.mainloop()
