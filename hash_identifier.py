import tkinter as tk
import re
from tkinter import filedialog

from shared import *


def analyze_hash_value(hash_value):
    results = ""

    if re.fullmatch(r"[a-fA-F0-9]{32}", hash_value):
        results += "[+] Possible: MD5\n"
        results += "[+] Possible: NTLM\n"

    elif re.fullmatch(r"[a-fA-F0-9]{40}", hash_value):
        results += "[+] Possible: SHA1\n"

    elif re.fullmatch(r"[a-fA-F0-9]{64}", hash_value):
        results += "[+] Possible: SHA256\n"

    elif re.fullmatch(r"[a-fA-F0-9]{128}", hash_value):
        results += "[+] Possible: SHA512\n"

    else:
        results += "[-] Unknown hash type.\n"

    return results


def create_hash_tab(notebook):

    hash_tab = tk.Frame(notebook, bg=BG)
    notebook.add(hash_tab, text="Hash Identifier")

    make_label(hash_tab, "HASH IDENTIFIER TOOL")
    make_subtitle(hash_tab, "Analyze and identify possible hash types")

    hash_entry = make_entry(hash_tab)

    result_text = make_text(hash_tab)

    def identify_hash():
        hash_value = hash_entry.get().strip()

        result_text.delete("1.0", tk.END)

        if not hash_value:
            result_text.insert(tk.END, "Please enter a hash.\n", "bad")
            return

        result_text.insert(tk.END, f"Analyzing hash:\n{hash_value}\n\n")
        result_text.insert(tk.END, analyze_hash_value(hash_value))

    def upload_hash_file():
        file_path = filedialog.askopenfilename(
            title="Select Hash Text File",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Loaded file: {file_path}\n\n")

        try:
            with open(file_path, "r") as file:
                hashes = file.readlines()

            for hash_value in hashes:
                hash_value = hash_value.strip()

                if hash_value:
                    result_text.insert(tk.END, f"Hash: {hash_value}\n")
                    result_text.insert(tk.END, analyze_hash_value(hash_value))
                    result_text.insert(tk.END, "\n-------------------------\n")

        except Exception as e:
            result_text.insert(tk.END, f"Error reading file: {e}\n", "bad")

    def export_hash_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("Hash Identifier Report", content)

    button_frame = tk.Frame(hash_tab, bg=BG)
    button_frame.pack()

    identify_button = make_button(button_frame, "Identify", identify_hash, green=True)
    identify_button.pack(side="left", padx=10)

    upload_button = make_button(button_frame, "Upload TXT", upload_hash_file)
    upload_button.pack(side="left", padx=10)

    export_button = make_button(button_frame, "Export PDF", export_hash_pdf)
    export_button.pack(side="left", padx=10)