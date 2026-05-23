import tkinter as tk
import requests

from backend.history import save_scan
from shared import *


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 30:
        return "D"
    return "F"


def create_http_headers_tab(notebook):

    headers_tab = tk.Frame(notebook, bg=BG)
    notebook.add(headers_tab, text="HTTP Headers")

    make_label(headers_tab, "HTTP HEADERS SCANNER")
    make_subtitle(headers_tab, "Analyze website security headers and generate a grade")

    url_entry = make_entry(headers_tab)
    result_text = make_text(headers_tab)

    def scan_headers():
        url = url_entry.get().strip()

        if not url:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Please enter a website URL.\n", "bad")
            return

        if not url.startswith("http"):
            url = "https://" + url

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Scanning website headers...\n")

        run_in_thread(lambda: finish_scan_headers(url))

    def finish_scan_headers(url):
        try:
            response = requests.get(url, timeout=7)
            headers = response.headers

            security_headers = {
                "Content-Security-Policy": "Helps prevent XSS attacks",
                "Strict-Transport-Security": "Forces HTTPS connections",
                "X-Frame-Options": "Protects against clickjacking",
                "X-Content-Type-Options": "Prevents MIME sniffing",
                "Referrer-Policy": "Controls referrer information sharing"
            }

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Scanning: {url}\n\n")

            score = 0

            for header, description in security_headers.items():
                if header in headers:
                    result_text.insert(tk.END, f"[+] {header} FOUND\n", "good")
                    result_text.insert(tk.END, f"    {description}\n\n")
                    score += 20
                else:
                    result_text.insert(tk.END, f"[-] {header} MISSING\n", "bad")
                    result_text.insert(tk.END, f"    {description}\n\n")

            grade = get_grade(score)

            result_text.insert(tk.END, f"\nSecurity Score: {score}/100\n")
            result_text.insert(tk.END, f"Security Grade: {grade}\n")

            save_scan("HTTP Headers Scanner", url, result_text.get("1.0", tk.END))

        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Could not scan website:\n{e}\n", "bad")

    def export_headers_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("HTTP Headers Scanner Report", content)

    button_frame = tk.Frame(headers_tab, bg=BG)
    button_frame.pack()

    scan_button = make_button(button_frame, "Scan Website", scan_headers, green=True)
    scan_button.pack(side="left", padx=10)

    export_button = make_button(button_frame, "Export PDF", export_headers_pdf)
    export_button.pack(side="left", padx=10)