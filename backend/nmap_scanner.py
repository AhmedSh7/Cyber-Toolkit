import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import shutil

from shared import *
from backend.history import save_scan


def create_nmap_scanner_tab(notebook):
    nmap_tab = tk.Frame(notebook, bg=BG)
    notebook.add(nmap_tab, text="Nmap")

    make_label(nmap_tab, "NMAP SCANNER")
    make_subtitle(nmap_tab, "Advanced scan using Nmap. Only scan systems you own or have permission to test.")

    target_entry = make_entry(nmap_tab)
    target_entry.insert(0, "127.0.0.1")

    result_text = make_text(nmap_tab)

    def run_nmap_scan():
        target = target_entry.get().strip()

        if not target:
            messagebox.showwarning("Input Error", "Please enter a target like 127.0.0.1 or example.com.")
            return

        if shutil.which("nmap") is None:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Nmap is not installed or not found in PATH.\n")
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Running Nmap scan...\n")
        result_text.insert(tk.END, "Only scan systems you own or have permission to test.\n\n")

        try:
            command = ["nmap", "-sV", "-T3", target]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout if result.stdout else result.stderr

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, output)

            save_scan("Nmap Scanner", target, output)

        except subprocess.TimeoutExpired:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Nmap scan timed out. Try a smaller target or simpler scan.\n")

        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Nmap scan failed:\n{e}")

    def run_thread():
        threading.Thread(target=run_nmap_scan, daemon=True).start()

    button_frame = tk.Frame(nmap_tab, bg=BG)
    button_frame.pack(pady=15)

    make_button(button_frame, "Run Nmap", run_thread, green=True).pack(side="left", padx=10)