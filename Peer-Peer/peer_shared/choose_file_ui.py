import tkinter as tk
from tkinter import filedialog 
import easygui
import easygui
import tkinter as tk
import os

def choose_torrent_file(default_path="."):
    # Tạo root để hiện icon dưới taskbar
    root = tk.Tk()
    root.iconify()  # thu nhỏ nhưng giúp hệ điều hành hiện icon

    file_path = easygui.fileopenbox(
        msg="Chọn file .torrent",
        title="Chọn torrent",
        default=os.path.join(default_path, "*.torrent"),
        filetypes=["*.torrent"]
    )

    root.destroy()
    return file_path


def choose_save_dir(default_path="."):
    root = tk.Tk()
    root.iconify()

    folder_path = easygui.diropenbox(
        msg="Chọn thư mục để lưu file",
        title="Chọn thư mục",
        default=default_path
    )

    root.destroy()
    return folder_path

def get_user_command():
    command_holder = {"value": None}

    def on_submit(event = None):
        command_holder["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Agent Command")
    root.geometry("300x120")

    label = tk.Label(root, text="Enter command (uploadfile /    downloadfile    / exit):")
    label.pack(pady=10)

    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus()
    entry.bind("<Return>", on_submit)
    button = tk.Button(root, text="Submit", command=on_submit)
    button.pack(pady=5)

    root.mainloop()
    return command_holder["value"]

def get_port():
    port_holder = {"value": None}

    def on_submit(event = None):
        port_holder["value"] = entry.get()
        root.quit()  # thoát mainloop đúng cách
        root.destroy()

    root = tk.Tk()
    root.title("Enter Upload Port")
    root.geometry("300x120")

    label = tk.Label(root, text="Enter server port:")
    label.pack(pady=10)

    entry = tk.Entry(root)
    entry.pack(pady=5)
    entry.focus()
    entry.bind("<Return>", on_submit)
    button = tk.Button(root, text="Submit", command=on_submit)
    button.pack(pady=5)

    root.mainloop()

    return port_holder["value"]