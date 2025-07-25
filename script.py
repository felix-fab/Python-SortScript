import os
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_FILENAME_LENGTH = 255

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def rename_files_with_path_prefix():
    base_folder = folder_path.get()
    if not os.path.isdir(base_folder):
        messagebox.showerror("Fehler", "Bitte wähle einen gültigen Ordner aus.")
        return

    renamed_files = 0

    try:
        for root, dirs, files in os.walk(base_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, base_folder)
                prefix = rel_path.replace(os.sep, "_")

                if prefix.strip() == ".":
                    continue

                if file.startswith(prefix + "_"):
                    continue

                new_name = f"{prefix}_{file}"
                new_path = os.path.join(root, new_name)

                if os.path.exists(new_path):
                    continue

                if len(new_name) > MAX_FILENAME_LENGTH:
                    messagebox.showinfo("Warnung", f"Dateiname zu lang: {new_name}")
                    continue

                os.rename(full_path, new_path)
                renamed_files += 1

        messagebox.showinfo("Fertig", f"{renamed_files} Datei(en) erfolgreich umbenannt.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Umbenennen:\n{str(e)}")

root = tk.Tk()
root.title("Dateinamen mit Pfadpräfix")
root.geometry("450x150")
root.resizable(False, False)

folder_path = tk.StringVar()

tk.Label(root, text="Ordner auswählen:").pack(pady=10)
tk.Entry(root, textvariable=folder_path, width=50).pack()
tk.Button(root, text="Durchsuchen...", command=choose_folder).pack(pady=5)
tk.Button(root, text="Dateien umbenennen", command=rename_files_with_path_prefix, bg="#007ACC", fg="white").pack(pady=10)

root.mainloop()