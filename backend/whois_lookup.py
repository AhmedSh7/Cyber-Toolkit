import tkinter as tk
import whois

from backend.history import save_scan
from shared import *


def create_whois_tab(notebook):

    whois_tab = tk.Frame(notebook, bg=BG)
    notebook.add(whois_tab, text="WHOIS Lookup")

    make_label(whois_tab, "WHOIS LOOKUP")
    make_subtitle(whois_tab, "Look up public domain registration information")

    whois_entry = make_entry(whois_tab)
    result_text = make_text(whois_tab)

    def run_whois():
        domain = whois_entry.get().strip()

        if not domain:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Please enter a domain.\n", "bad")
            return

        domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Running WHOIS lookup...\n")

        run_in_thread(lambda: finish_whois(domain))

    def finish_whois(domain):
        try:
            data = whois.whois(domain)

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"WHOIS Lookup: {domain}\n\n")
            result_text.insert(tk.END, f"Domain Name: {data.domain_name}\n")
            result_text.insert(tk.END, f"Registrar: {data.registrar}\n")
            result_text.insert(tk.END, f"Creation Date: {data.creation_date}\n")
            result_text.insert(tk.END, f"Expiration Date: {data.expiration_date}\n")
            result_text.insert(tk.END, f"Name Servers: {data.name_servers}\n")

        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"WHOIS lookup failed:\n{e}\n", "bad")
            save_scan("WHOIS Lookup", domain, result_text.get("1.0", tk.END))

    def export_whois_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("WHOIS Lookup Report", content)

    button_frame = tk.Frame(whois_tab, bg=BG)
    button_frame.pack()

    make_button(button_frame, "Run WHOIS", run_whois, green=True).pack(side="left", padx=10)
    make_button(button_frame, "Export PDF", export_whois_pdf).pack(side="left", padx=10)