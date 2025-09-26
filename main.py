import tkinter as tk
from tkinter import filedialog, messagebox
import os
from qr_reader import process_all_pdfs  # 処理関数（別ファイルに分離）

class QRSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR答案仕分けツール")
        self.root.geometry("500x300")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar(value="採点用")

        # 入力フォルダ選択
        tk.Label(root, text="スキャン済みPDFフォルダ").pack(pady=5)
        tk.Entry(root, textvariable=self.input_dir, width=50).pack()
        tk.Button(root, text="フォルダ選択", command=self.select_folder).pack(pady=5)

        # 実行ボタン
        tk.Button(root, text="QR読み取り＆仕分け実行", command=self.run_sorting).pack(pady=10)

        # 出力先表示
        tk.Label(root, text="出力先フォルダ").pack()
        tk.Entry(root, textvariable=self.output_dir, width=50).pack()

        # ログ表示
        self.log_box = tk.Text(root, height=8, width=60)
        self.log_box.pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_dir.set(folder)

    def run_sorting(self):
        input_path = self.input_dir.get()
        output_path = self.output_dir.get()
        if not os.path.isdir(input_path):
            messagebox.showerror("エラー", "有効なフォルダを選択してください")
            return
        self.log_box.insert(tk.END, f"処理開始：{input_path}\n")
        try:
            count = process_all_pdfs(input_path, output_path, self.log_box)
            self.log_box.insert(tk.END, f"完了：{count}件のPDFを仕分けしました\n")
        except Exception as e:
            self.log_box.insert(tk.END, f"エラー：{str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRSorterApp(root)
    root.mainloop()
