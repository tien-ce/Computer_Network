import tkinter as tk
from tkinter import filedialog 

def choose_torrent_file(root_path):
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_path = filedialog.askopenfilename(
        initialdir=root_path,
        title="Select a .torrent file",
        filetypes=(("Torrent files", "*.torrent"), ("All files", "*.*"))
    )
    root.destroy()
    return file_path

def choose_save_dir(root_path):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(
        initialdir=root_path,
        title="Select folder to save file"
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