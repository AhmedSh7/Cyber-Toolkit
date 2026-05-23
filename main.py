import tkinter as tk
from tkinter import ttk

from shared import BG, GREEN

from backend.hash_identifier import create_hash_tab
from backend.http_headers import create_http_headers_tab
from backend.breach_checker import create_breach_checker_tab
from backend.whois_lookup import create_whois_tab
from backend.dns_lookup import create_dns_tab
from backend.port_scanner import create_port_scanner_tab
from backend.cve_search import create_cve_search_tab
from backend.subdomain_enum import create_subdomain_tab
from backend.history import create_history_tab


root = tk.Tk()
root.title("Cyber Toolkit")
root.geometry("850x650")
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "TNotebook",
    background=BG,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background="#1a1a1a",
    foreground=GREEN,
    padding=[10, 5],
    font=("Arial", 10, "bold")
)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

create_hash_tab(notebook)
create_http_headers_tab(notebook)
create_breach_checker_tab(notebook)
create_whois_tab(notebook)
create_dns_tab(notebook)
create_port_scanner_tab(notebook)
create_cve_search_tab(notebook)
create_subdomain_tab(notebook)
create_history_tab(notebook)

root.mainloop()