import tkinter as tk
from tkinter import messagebox
import requests
import threading

from shared import *
from backend.history import save_scan


def create_subdomain_tab(notebook):
    subdomain_tab = tk.Frame(notebook, bg=BG)
    notebook.add(subdomain_tab, text="Subdomains")

    make_label(subdomain_tab, "PASSIVE SUBDOMAIN ENUMERATION")
    make_subtitle(
        subdomain_tab,
        "Find public subdomains using certificate transparency logs"
    )

    domain_entry = make_entry(subdomain_tab)
    result_text = make_text(subdomain_tab)

    def find_subdomains():
        domain = domain_entry.get().strip().lower()

        if not domain:
            messagebox.showwarning(
                "Input Error",
                "Please enter a domain like example.com"
            )
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "Searching public certificate logs...\n"
        )

        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=40
            )

            response.raise_for_status()

            data = response.json()
            subdomains = set()

            for entry in data:
                name_value = entry.get("name_value", "")
                names = name_value.split("\n")

                for name in names:
                    clean_name = name.strip().lower()
                    clean_name = clean_name.replace("*.", "")

                    if clean_name.endswith(domain):
                        subdomains.add(clean_name)

            result_text.delete("1.0", tk.END)

            if not subdomains:
                result_text.insert(
                    tk.END,
                    "No subdomains found."
                )
                return

            final_result = (
                f"Passive Subdomain Enumeration: {domain}\n\n"
            )

            final_result += (
                f"Total Subdomains Found: "
                f"{len(subdomains)}\n\n"
            )

            for subdomain in sorted(subdomains):
                final_result += f"- {subdomain}\n"

            result_text.insert(tk.END, final_result)

            save_scan(
                "Subdomain Enumeration",
                domain,
                final_result
            )

        except requests.exceptions.Timeout:
            result_text.delete("1.0", tk.END)
            result_text.insert(
                tk.END,
                "Request timed out.\n\n"
                "The public certificate source may be slow "
                "or overloaded.\n"
                "Try again later or test with a smaller "
                "domain like mozilla.org."
            )

        except requests.exceptions.HTTPError:
            result_text.delete("1.0", tk.END)
            result_text.insert(
                tk.END,
                "The public certificate source returned "
                "an error.\n\n"
                "This can happen with large domains or "
                "temporary crt.sh issues.\n"
                "Try again later or test with another domain."
            )

        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(
                tk.END,
                f"Error finding subdomains:\n{e}"
            )

    def export_subdomain_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("Subdomain Enumeration Report", content)

    def run_thread():
        threading.Thread(
            target=find_subdomains,
            daemon=True
        ).start()

    button_frame = tk.Frame(subdomain_tab, bg=BG)
    button_frame.pack(pady=15)

    make_button(button_frame, "Find Subdomains", run_thread, green=True).pack(side="left", padx=10)
    make_button(button_frame, "Export PDF", export_subdomain_pdf).pack(side="left", padx=10)
