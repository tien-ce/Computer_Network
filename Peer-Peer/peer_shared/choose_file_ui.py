import tkinter as tk
from tkinter import filedialog

def choose_torrent_file(initial_dir):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file .torrent",
        filetypes=[("Torrent files", "*.torrent")],
        initialdir=initial_dir
    )
    return file_path
