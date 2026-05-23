import tkinter as tk
import hashlib
import requests

from shared import *


def create_breach_checker_tab(notebook):

    breach_tab = tk.Frame(notebook, bg=BG)
    notebook.add(breach_tab, text="Breach Checker")

    make_label(breach_tab, "PASSWORD BREACH CHECKER")
    make_subtitle(breach_tab, "Safely checks password exposure using SHA1 k-anonymity")

    password_entry = make_entry(breach_tab, show="*")
    result_text = make_text(breach_tab)

    def check_password_breach():
        password = password_entry.get().strip()

        if not password:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Please enter a password.\n", "bad")
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Checking password exposure safely...\n")

        run_in_thread(lambda: finish_password_check(password))

    def finish_password_check(password):
        try:
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]

            response = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                timeout=7
            )

            if response.status_code != 200:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Could not check password at this time.\n", "bad")
                return

            found_count = 0

            for line in response.text.splitlines():
                hash_suffix, count = line.split(":")
                if hash_suffix == suffix:
                    found_count = int(count)
                    break

            result_text.delete("1.0", tk.END)

            if found_count > 0:
                result_text.insert(tk.END, "[!] Password found in known breaches.\n", "bad")
                result_text.insert(tk.END, f"Seen approximately {found_count} times.\n\n")
                result_text.insert(tk.END, "Recommendation:\n")
                result_text.insert(tk.END, "Use a unique, stronger password and enable MFA.\n")
            else:
                result_text.insert(tk.END, "[+] Password was not found in known breach data.\n", "good")
                result_text.insert(tk.END, "Still use a unique password and MFA when possible.\n")

        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Could not check password:\n{e}\n", "bad")

    def export_breach_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("Password Breach Checker Report", content)

    button_frame = tk.Frame(breach_tab, bg=BG)
    button_frame.pack()

    check_button = make_button(button_frame, "Check Password", check_password_breach, green=True)
    check_button.pack(side="left", padx=10)

    export_button = make_button(button_frame, "Export PDF", export_breach_pdf)
    export_button.pack(side="left", padx=10)