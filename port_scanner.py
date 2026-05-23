import tkinter as tk
import socket

from shared import *


def create_port_scanner_tab(notebook):

    port_tab = tk.Frame(notebook, bg=BG)
    notebook.add(port_tab, text="Port Scanner")

    make_label(port_tab, "BASIC PORT SCANNER")
    make_subtitle(port_tab, "Only scan systems you own or have permission to test")

    target_entry = make_entry(port_tab)
    target_entry.insert(0, "127.0.0.1")

    ports_entry = make_entry(port_tab)
    ports_entry.insert(0, "22,80,443")

    result_text = make_text(port_tab)

    def scan_ports():
        target = target_entry.get().strip()
        ports_text = ports_entry.get().strip()

        if not target:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Please enter a target.\n", "bad")
            return

        try:
            ports = [int(port.strip()) for port in ports_text.split(",")]
        except ValueError:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Ports must be numbers separated by commas.\n", "bad")
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[*] Starting basic port scan...\n")
        result_text.insert(tk.END, "Only scan systems you own or have permission to test.\n\n")

        run_in_thread(lambda: finish_port_scan(target, ports))

    def finish_port_scan(target, ports):
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))

                if result == 0:
                    result_text.insert(tk.END, f"[+] Port {port} is OPEN\n", "good")
                else:
                    result_text.insert(tk.END, f"[-] Port {port} is CLOSED/FILTERED\n", "bad")

                sock.close()

            except Exception as e:
                result_text.insert(tk.END, f"[-] Error scanning port {port}: {e}\n", "bad")

    def export_port_pdf():
        content = result_text.get("1.0", tk.END)
        write_pdf("Port Scanner Report", content)

    button_frame = tk.Frame(port_tab, bg=BG)
    button_frame.pack()

    make_button(button_frame, "Scan Ports", scan_ports, green=True).pack(side="left", padx=10)
    make_button(button_frame, "Export PDF", export_port_pdf).pack(side="left", padx=10)