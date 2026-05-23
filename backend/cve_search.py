import tkinter as tk
from tkinter import messagebox
import requests
import threading

from shared import *
from backend.history import save_scan


def create_cve_search_tab(notebook):
    cve_tab = tk.Frame(notebook, bg=BG)
    notebook.add(cve_tab, text="CVE Search")

    make_label(cve_tab, "CVE SEARCH TOOL")
    make_subtitle(cve_tab, "Search known vulnerabilities by product or keyword")

    keyword_entry = make_entry(cve_tab)
    result_text = make_text(cve_tab)

    def search_cves():
        keyword = keyword_entry.get().strip()

        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword like Apache, OpenSSL, Windows, or Log4j.")
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Searching CVE database...\n")

        try:
            url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
            params = {
                "keywordSearch": keyword,
                "resultsPerPage": 10
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            vulnerabilities = data.get("vulnerabilities", [])

            result_text.delete("1.0", tk.END)

            if not vulnerabilities:
                result_text.insert(tk.END, "No CVEs found for this keyword.")
                return

            final_result = ""

            for item in vulnerabilities:
                cve = item.get("cve", {})
                cve_id = cve.get("id", "N/A")
                published = cve.get("published", "N/A")

                descriptions = cve.get("descriptions", [])
                description = "No description available."

                for desc in descriptions:
                    if desc.get("lang") == "en":
                        description = desc.get("value", "No description available.")
                        break

                severity = "N/A"
                metrics = cve.get("metrics", {})

                if "cvssMetricV31" in metrics:
                    severity = metrics["cvssMetricV31"][0]["cvssData"].get("baseSeverity", "N/A")
                elif "cvssMetricV30" in metrics:
                    severity = metrics["cvssMetricV30"][0]["cvssData"].get("baseSeverity", "N/A")
                elif "cvssMetricV2" in metrics:
                    severity = metrics["cvssMetricV2"][0].get("baseSeverity", "N/A")

                cve_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"

                final_result += f"CVE ID: {cve_id}\n"
                final_result += f"Severity: {severity}\n"
                final_result += f"Published: {published}\n"
                final_result += f"Description: {description}\n"
                final_result += f"Link: {cve_link}\n"
                final_result += "-" * 80 + "\n\n"

            result_text.insert(tk.END, final_result)

            save_scan("CVE Search", keyword, final_result)

        except requests.exceptions.RequestException as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error searching CVEs:\n{e}")

    def run_thread():
        threading.Thread(target=search_cves, daemon=True).start()

    button_frame = tk.Frame(cve_tab, bg=BG)
    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Search CVEs",
        command=run_thread,
        font=("Arial", 10, "bold"),
        fg=GREEN,
        width=20
    ).pack()