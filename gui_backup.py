import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.pdfgen import canvas
import datetime
import requests

def scan_headers():

    url = url_entry.get().strip()

    if not url.startswith("http"):
        url = "https://" + url

    headers_result.delete("1.0", tk.END)

    try:
        response = requests.get(url, timeout=5)

        headers = response.headers

        security_headers = {
            "Content-Security-Policy":
                "Helps prevent XSS attacks",

            "Strict-Transport-Security":
                "Forces HTTPS connections",

            "X-Frame-Options":
                "Protects against clickjacking",

            "X-Content-Type-Options":
                "Prevents MIME sniffing",

            "Referrer-Policy":
                "Controls referrer information sharing"
        }

        headers_result.insert(
            tk.END,
            f"Scanning: {url}\n\n"
        )

        score = 0

        for header, description in security_headers.items():

            if header in headers:
                headers_result.insert(
                    tk.END,
                    f"[+] {header} FOUND\n"
                )

                headers_result.insert(
                    tk.END,
                    f"    {description}\n\n"
                )

                score += 20

            else:
                headers_result.insert(
                    tk.END,
                    f"[-] {header} MISSING\n"
                )

                headers_result.insert(
                    tk.END,
                    f"    {description}\n\n"
                )

        headers_result.insert(
            tk.END,
            f"\nSecurity Score: {score}/100\n"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not scan website:\n{e}"
        )

def identify_hash():
    hash_value = hash_entry.get().strip()
    hash_length = len(hash_value)

    hash_types = {
        32: ["MD5", "MD4", "NTLM"],
        40: ["SHA1", "RIPEMD-160"],
        56: ["SHA224"],
        64: ["SHA256", "SHA3-256", "BLAKE2s"],
        96: ["SHA384"],
        128: ["SHA512", "SHA3-512", "BLAKE2b"]
    }

    hash_result.delete("1.0", tk.END)

    if hash_length in hash_types:
        hash_result.insert(tk.END, "Possible hash type(s):\n\n")

        for hash_type in hash_types[hash_length]:
            hash_result.insert(tk.END, f"[+] {hash_type}\n")
    else:
        hash_result.insert(tk.END, "[-] Unknown hash type")


def export_pdf():
    results = hash_result.get("1.0", tk.END).strip()

    if not results:
        messagebox.showwarning("Warning", "No results to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    pdf = canvas.Canvas(file_path)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "Cyber Toolkit Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        50,
        775,
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    y = 730

    for line in results.split("\n"):
        pdf.drawString(50, y, line)
        y -= 20

    pdf.save()

    messagebox.showinfo("Success", "PDF report exported successfully.")


# Main Window
root = tk.Tk()
root.title("Cyber Toolkit")
root.geometry("750x550")
root.configure(bg="#0d0d0d")

# Style
style = ttk.Style()
style.theme_use("default")

style.configure(
    "TNotebook",
    background="#0d0d0d",
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background="#1a1a1a",
    foreground="#00ff41",
    padding=[10, 5],
    font=("Arial", 11, "bold")
)

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# HASH IDENTIFIER TAB
hash_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(hash_tab, text="Hash Identifier")

# FUTURE TAB
headers_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(headers_tab, text="HTTP Headers Scanner")

title = tk.Label(
    hash_tab,
    text="CYBER TOOLKIT",
    font=("Arial", 24, "bold"),
    fg="#00ff41",
    bg="#0d0d0d"
)
title.pack(pady=20)

subtitle = tk.Label(
    hash_tab,
    text="Hash Identifier Module",
    font=("Arial", 12),
    fg="#777777",
    bg="#0d0d0d"
)
subtitle.pack()

hash_entry = tk.Entry(
    hash_tab,
    width=60,
    font=("Arial", 13),
    bg="#1a1a1a",
    fg="#00ff41",
    insertbackground="#00ff41"
)
hash_entry.pack(pady=15)

button_frame = tk.Frame(hash_tab, bg="#0d0d0d")
button_frame.pack()

identify_button = tk.Button(
    button_frame,
    text="Identify",
    command=identify_hash,
    bg="#00ff41",
    fg="black",
    font=("Arial", 11, "bold"),
    width=12
)
identify_button.grid(row=0, column=0, padx=5)

pdf_button = tk.Button(
    button_frame,
    text="Export PDF",
    command=export_pdf,
    bg="#1a1a1a",
    fg="#00ff41",
    font=("Arial", 11, "bold"),
    width=12
)
pdf_button.grid(row=0, column=1, padx=5)

hash_result = tk.Text(
    hash_tab,
    width=75,
    height=18,
    bg="#050505",
    fg="#00ff41",
    font=("Courier", 12),
    insertbackground="#00ff41"
)
hash_result.pack(pady=20)

headers_title = tk.Label(
    headers_tab,
    text="HTTP HEADERS SCANNER",
    font=("Arial", 22, "bold"),
    fg="#00ff41",
    bg="#0d0d0d"
)
headers_title.pack(pady=20)

headers_subtitle = tk.Label(
    headers_tab,
    text="Analyze website security headers",
    font=("Arial", 11),
    fg="#777777",
    bg="#0d0d0d"
)
headers_subtitle.pack()

url_entry = tk.Entry(
    headers_tab,
    width=60,
    font=("Arial", 13),
    bg="#1a1a1a",
    fg="#00ff41",
    insertbackground="#00ff41"
)
url_entry.pack(pady=15)

scan_headers_button = tk.Button(
    headers_tab,
    text="Scan Website",
    command=scan_headers,
    bg="#00ff41",
    fg="black",
    font=("Arial", 11, "bold"),
    width=16
)
scan_headers_button.pack()

headers_result = tk.Text(
    headers_tab,
    width=75,
    height=18,
    bg="#050505",
    fg="#00ff41",
    font=("Courier", 11),
    insertbackground="#00ff41"
)
headers_result.pack(pady=20)

root.mainloop()