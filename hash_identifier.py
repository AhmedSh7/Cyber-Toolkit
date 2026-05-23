import tkinter as tk
import re

from shared import *


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

        found = False

        if re.fullmatch(r"[a-fA-F0-9]{32}", hash_value):
            result_text.insert(tk.END, "[+] Possible: MD5\n", "good")
            result_text.insert(tk.END, "[+] Possible: NTLM\n", "good")
            found = True

        if re.fullmatch(r"[a-fA-F0-9]{40}", hash_value):
            result_text.insert(tk.END, "[+] Possible: SHA1\n", "good")
            found = True

        if re.fullmatch(r"[a-fA-F0-9]{64}", hash_value):
            result_text.insert(tk.END, "[+] Possible: SHA256\n", "good")
            found = True

        if re.fullmatch(r"[a-fA-F0-9]{128}", hash_value):
            result_text.insert(tk.END, "[+] Possible: SHA512\n", "good")
            found = True

        if not found:
            result_text.insert(tk.END, "[-] Unknown hash type.\n", "bad")

    def export_hash_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("Hash Identifier Report", content)

    button_frame = tk.Frame(hash_tab, bg=BG)
    button_frame.pack()

    identify_button = make_button(button_frame, "Identify", identify_hash, green=True)
    identify_button.pack(side="left", padx=10)

    export_button = make_button(button_frame, "Export PDF", export_hash_pdf)
    export_button.pack(side="left", padx=10)