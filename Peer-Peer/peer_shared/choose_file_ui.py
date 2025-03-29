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
    root.destroy()
    return file_path
def choose_save_dir(initial_dir):
    root = tk.Tk()
    root.withdraw()
    savedir = filedialog.askdirectory(
        title="Chọn thư mục để lưu file",
        initialdir=initial_dir
    )
    root.destroy()
    return savedir
def get_user_command():
    command_holder = {"value": None}

    def on_submit():
        command_holder["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Agent Command")
    root.geometry("300x120")

    label = tk.Label(root, text="Enter command (uploadfile / exit):")
    label.pack(pady=10)

    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus()

    button = tk.Button(root, text="Submit", command=on_submit)
    button.pack(pady=5)

    root.mainloop()
    return command_holder["value"]

def get_port():
    port_holder = {"value": None}

    def on_submit():
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

    button = tk.Button(root, text="Submit", command=on_submit)
    button.pack(pady=5)

    root.mainloop()

    return port_holder["value"]