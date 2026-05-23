import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
import datetime
import threading


BG = "#0d0d0d"
BOX_BG = "#050505"
ENTRY_BG = "#1a1a1a"
GREEN = "#00ff41"
RED = "#ff3333"
GRAY = "#777777"


def run_in_thread(function):
    thread = threading.Thread(target=function)
    thread.daemon = True
    thread.start()


def write_pdf(title, content):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    pdf = canvas.Canvas(file_path)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, title)

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, 775, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 740
    for line in content.split("\n"):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 800
        pdf.drawString(50, y, line[:95])
        y -= 16

    pdf.save()
    messagebox.showinfo("Success", "PDF exported successfully.")


def make_label(parent, text, size=22):
    label = tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold"),
        fg=GREEN,
        bg=BG
    )
    label.pack(pady=20)
    return label


def make_subtitle(parent, text):
    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 11),
        fg=GRAY,
        bg=BG
    )
    label.pack()
    return label


def make_entry(parent, width=60, show=None):
    entry = tk.Entry(
        parent,
        width=width,
        font=("Arial", 13),
        bg=ENTRY_BG,
        fg=GREEN,
        insertbackground=GREEN,
        show=show
    )
    entry.pack(pady=15)
    return entry


def make_text(parent, height=20):
    text = tk.Text(
        parent,
        height=height,
        width=80,
        bg=BOX_BG,
        fg=GREEN,
        insertbackground=GREEN,
        wrap="word",
        font=("Courier", 10, "bold")
    )

    text.tag_config("good", foreground=GREEN)
    text.tag_config("bad", foreground=RED)
    text.pack(pady=20)
    return text


def make_button(parent, text, command, green=False):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=GREEN if green else ENTRY_BG,
        fg="black" if green else GREEN,
        font=("Arial", 11, "bold"),
        width=16
    )