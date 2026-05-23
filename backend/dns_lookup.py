import tkinter as tk
import dns.resolver

from backend.history import save_scan
from shared import *


def create_dns_tab(notebook):

    dns_tab = tk.Frame(notebook, bg=BG)
    notebook.add(dns_tab, text="DNS Lookup")

    make_label(dns_tab, "DNS LOOKUP")
    make_subtitle(dns_tab, "Look up DNS records for a domain")

    dns_entry = make_entry(dns_tab)
    dns_entry.insert(0, "github.com")

    result_text = make_text(dns_tab)

    def run_dns_lookup():
        domain = dns_entry.get().strip()

        if not domain:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Please enter a domain.\n", "bad")
            return

        domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Running DNS lookup...\n")

        run_in_thread(lambda: finish_dns_lookup(domain))

    def finish_dns_lookup(domain):
        record_types = ["A", "AAAA", "MX", "NS", "TXT"]

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"DNS Lookup: {domain}\n\n")

        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                result_text.insert(tk.END, f"{record_type} Records:\n", "good")

                for answer in answers:
                    result_text.insert(tk.END, f"  {answer}\n")

                result_text.insert(tk.END, "\n")

            except Exception:
                result_text.insert(tk.END, f"{record_type} Records: Not found\n\n", "bad")
                save_scan("DNS Lookup", domain, result_text.get("1.0", tk.END))

    def export_dns_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("DNS Lookup Report", content)

    button_frame = tk.Frame(dns_tab, bg=BG)
    button_frame.pack()

    make_button(button_frame, "Run DNS Lookup", run_dns_lookup, green=True).pack(side="left", padx=10)
    make_button(button_frame, "Export PDF", export_dns_pdf).pack(side="left", padx=10)