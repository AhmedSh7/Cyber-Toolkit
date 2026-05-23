import tkinter as tk
import sqlite3
import datetime

from shared import *


DB_NAME = "scan_history.db"


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT,
            target TEXT,
            result TEXT,
            scan_time TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_scan(tool_name, target, result):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO history (tool_name, target, result, scan_time)
        VALUES (?, ?, ?, ?)
    """, (
        tool_name,
        target,
        result,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def create_history_tab(notebook):
    initialize_database()

    history_tab = tk.Frame(notebook, bg=BG)
    notebook.add(history_tab, text="Scan History")

    make_label(history_tab, "SCAN HISTORY")
    make_subtitle(history_tab, "View locally saved scan results")

    result_text = make_text(history_tab)

    def load_history():
        result_text.delete("1.0", tk.END)

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT tool_name, target, result, scan_time
            FROM history
            ORDER BY id DESC
            LIMIT 50
        """)

        rows = cursor.fetchall()
        connection.close()

        if not rows:
            result_text.insert(tk.END, "No scan history found.\n")
            return

        for tool_name, target, result, scan_time in rows:
            result_text.insert(tk.END, f"Tool: {tool_name}\n", "good")
            result_text.insert(tk.END, f"Target: {target}\n")
            result_text.insert(tk.END, f"Time: {scan_time}\n")
            result_text.insert(tk.END, f"Result:\n{result}\n")
            result_text.insert(tk.END, "\n-------------------------\n")

    def clear_history():
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM history")
        connection.commit()
        connection.close()

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Scan history cleared.\n", "bad")

    button_frame = tk.Frame(history_tab, bg=BG)
    button_frame.pack()

    make_button(button_frame, "Load History", load_history, green=True).pack(side="left", padx=10)
    make_button(button_frame, "Clear History", clear_history).pack(side="left", padx=10)