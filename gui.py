import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.pdfgen import canvas
import datetime
import hashlib
import requests
import socket
import whois


# ---------- SHARED ----------

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


# ---------- HASH IDENTIFIER ----------

def is_valid_hex(hash_value):
    try:
        int(hash_value, 16)
        return True
    except ValueError:
        return False


def analyze_hash(hash_value):
    hash_value = hash_value.strip()
    hash_length = len(hash_value)

    hash_types = {
        32: ["MD5", "MD4", "NTLM"],
        40: ["SHA1", "RIPEMD-160"],
        56: ["SHA224"],
        64: ["SHA256", "SHA3-256", "BLAKE2s"],
        96: ["SHA384"],
        128: ["SHA512", "SHA3-512", "BLAKE2b"]
    }

    if not hash_value:
        return "[-] Empty hash value."

    if not is_valid_hex(hash_value):
        return "[-] Invalid hash. Only hexadecimal characters are allowed."

    if hash_length in hash_types:
        result = "Possible hash type(s):\n\n"
        for hash_type in hash_types[hash_length]:
            result += f"[+] {hash_type}\n"
        return result

    return "[-] Unknown hash type."


def identify_hash():
    hash_result.delete("1.0", tk.END)
    hash_result.insert(tk.END, "[*] Analyzing hash...\n")
    root.after(400, finish_identify_hash)


def finish_identify_hash():
    hash_value = hash_entry.get().strip()
    hash_result.delete("1.0", tk.END)
    hash_result.insert(tk.END, analyze_hash(hash_value))


def export_hash_pdf():
    content = hash_result.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No hash results to export.")
        return
    write_pdf("Cyber Toolkit - Hash Identifier Report", content)


# ---------- HTTP HEADERS ----------

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


def scan_headers():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a website URL.")
        return

    if not url.startswith("http"):
        url = "https://" + url

    headers_result.delete("1.0", tk.END)
    headers_result.insert(tk.END, "[*] Scanning website headers...\n")

    root.after(500, lambda: finish_scan_headers(url))


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

        headers_result.delete("1.0", tk.END)
        headers_result.insert(tk.END, f"Scanning: {url}\n\n")

        score = 0

        for header, description in security_headers.items():
            if header in headers:
                headers_result.insert(tk.END, f"[+] {header} FOUND\n", "good")
                headers_result.insert(tk.END, f"    {description}\n\n")
                score += 20
            else:
                headers_result.insert(tk.END, f"[-] {header} MISSING\n", "bad")
                headers_result.insert(tk.END, f"    {description}\n\n")

        grade = get_grade(score)
        headers_result.insert(tk.END, f"\nSecurity Score: {score}/100\n")
        headers_result.insert(tk.END, f"Security Grade: {grade}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Could not scan website:\n{e}")


def export_headers_pdf():
    content = headers_result.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No HTTP results to export.")
        return
    write_pdf("Cyber Toolkit - HTTP Headers Report", content)


# ---------- PASSWORD BREACH CHECKER ----------

def check_password_breach():
    password = password_entry.get().strip()

    if not password:
        messagebox.showerror("Error", "Please enter a password to check.")
        return

    breach_result.delete("1.0", tk.END)
    breach_result.insert(tk.END, "[*] Checking password exposure safely...\n")

    root.after(500, lambda: finish_password_check(password))


def finish_password_check(password):
    try:
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=7)

        if response.status_code != 200:
            breach_result.delete("1.0", tk.END)
            breach_result.insert(tk.END, "[-] Could not check password at this time.")
            return

        hashes = response.text.splitlines()
        found_count = 0

        for line in hashes:
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                found_count = int(count)
                break

        breach_result.delete("1.0", tk.END)

        if found_count > 0:
            breach_result.insert(tk.END, "[!] Password found in known breaches.\n", "bad")
            breach_result.insert(tk.END, f"Seen approximately {found_count} times.\n\n")
            breach_result.insert(tk.END, "Recommendation:\nUse a unique, stronger password and enable MFA.")
        else:
            breach_result.insert(tk.END, "[+] Password was not found in known breach data.\n", "good")
            breach_result.insert(tk.END, "Still use a unique password and MFA when possible.")

    except Exception as e:
        messagebox.showerror("Error", f"Could not check password:\n{e}")


# ---------- WHOIS LOOKUP ----------

def run_whois():
    domain = whois_entry.get().strip()

    if not domain:
        messagebox.showerror("Error", "Please enter a domain.")
        return

    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

    whois_result.delete("1.0", tk.END)
    whois_result.insert(tk.END, "[*] Running WHOIS lookup...\n")

    root.after(500, lambda: finish_whois(domain))


def finish_whois(domain):
    try:
        data = whois.whois(domain)

        whois_result.delete("1.0", tk.END)
        whois_result.insert(tk.END, f"WHOIS Lookup: {domain}\n\n")
        whois_result.insert(tk.END, f"Domain Name: {data.domain_name}\n")
        whois_result.insert(tk.END, f"Registrar: {data.registrar}\n")
        whois_result.insert(tk.END, f"Creation Date: {data.creation_date}\n")
        whois_result.insert(tk.END, f"Expiration Date: {data.expiration_date}\n")
        whois_result.insert(tk.END, f"Name Servers: {data.name_servers}\n")

    except Exception as e:
        messagebox.showerror("Error", f"WHOIS lookup failed:\n{e}")


# ---------- PORT SCANNER ----------

def scan_ports():
    target = port_target_entry.get().strip()
    ports_text = port_list_entry.get().strip()

    if not target:
        messagebox.showerror("Error", "Please enter a target.")
        return

    if not ports_text:
        ports = [22, 80, 443]
    else:
        try:
            ports = [int(p.strip()) for p in ports_text.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Ports must be numbers separated by commas.")
            return

    port_result.delete("1.0", tk.END)
    port_result.insert(tk.END, "[*] Starting basic port scan...\n")
    port_result.insert(tk.END, "Only scan systems you own or have permission to test.\n\n")

    root.after(500, lambda: finish_port_scan(target, ports))


def finish_port_scan(target, ports):
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))

            if result == 0:
                port_result.insert(tk.END, f"[+] Port {port} is OPEN\n", "good")
            else:
                port_result.insert(tk.END, f"[-] Port {port} is CLOSED/FILTERED\n", "bad")

            sock.close()

        except Exception as e:
            port_result.insert(tk.END, f"[-] Error scanning port {port}: {e}\n", "bad")


# ---------- UI HELPERS ----------

def make_label(parent, text, size=22):
    label = tk.Label(parent, text=text, font=("Arial", size, "bold"), fg="#00ff41", bg="#0d0d0d")
    label.pack(pady=20)
    return label


def make_subtitle(parent, text):
    label = tk.Label(parent, text=text, font=("Arial", 11), fg="#777777", bg="#0d0d0d")
    label.pack()
    return label


def make_entry(parent, width=60, show=None):
    entry = tk.Entry(parent, width=width, font=("Arial", 13), bg="#1a1a1a", fg="#00ff41",
                     insertbackground="#00ff41", show=show)
    entry.pack(pady=15)
    return entry


def make_text(parent, height=18):
    text = tk.Text(parent, width=78, height=height, bg="#050505", fg="#00ff41",
                   font=("Courier", 11), insertbackground="#00ff41")
    text.tag_config("good", foreground="#00ff41")
    text.tag_config("bad", foreground="#ff3333")
    text.pack(pady=20)
    return text


def make_button(parent, text, command, green=False):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg="#00ff41" if green else "#1a1a1a",
        fg="black" if green else "#00ff41",
        font=("Arial", 11, "bold"),
        width=16
    )


# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Cyber Toolkit")
root.geometry("850x650")
root.configure(bg="#0d0d0d")

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#0d0d0d", borderwidth=0)
style.configure("TNotebook.Tab", background="#1a1a1a", foreground="#00ff41", padding=[10, 5],
                font=("Arial", 10, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


# HASH TAB
hash_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(hash_tab, text="Hash Identifier")

make_label(hash_tab, "HASH IDENTIFIER")
make_subtitle(hash_tab, "Analyze hash length and possible algorithms")

hash_entry = make_entry(hash_tab)

hash_buttons = tk.Frame(hash_tab, bg="#0d0d0d")
hash_buttons.pack()

make_button(hash_buttons, "Identify", identify_hash, True).grid(row=0, column=0, padx=5)
make_button(hash_buttons, "Export PDF", export_hash_pdf).grid(row=0, column=1, padx=5)

hash_result = make_text(hash_tab)


# HTTP TAB
headers_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(headers_tab, text="HTTP Headers")

make_label(headers_tab, "HTTP HEADERS SCANNER")
make_subtitle(headers_tab, "Analyze website security headers and generate a grade")

url_entry = make_entry(headers_tab)

headers_buttons = tk.Frame(headers_tab, bg="#0d0d0d")
headers_buttons.pack()

make_button(headers_buttons, "Scan Website", scan_headers, True).grid(row=0, column=0, padx=5)
make_button(headers_buttons, "Export PDF", export_headers_pdf).grid(row=0, column=1, padx=5)

headers_result = make_text(headers_tab)
headers_result.tag_config("good", foreground="#00ff41")
headers_result.tag_config("bad", foreground="#ff3333")


# BREACH CHECKER TAB
breach_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(breach_tab, text="Breach Checker")

make_label(breach_tab, "PASSWORD BREACH CHECKER")
make_subtitle(breach_tab, "Safely checks password exposure using SHA1 k-anonymity")

password_entry = make_entry(breach_tab, show="*")

make_button(breach_tab, "Check Password", check_password_breach, True).pack()

breach_result = make_text(breach_tab)


# WHOIS TAB
whois_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(whois_tab, text="WHOIS Lookup")

make_label(whois_tab, "WHOIS LOOKUP")
make_subtitle(whois_tab, "Look up public domain registration information")

whois_entry = make_entry(whois_tab)

make_button(whois_tab, "Run WHOIS", run_whois, True).pack()

whois_result = make_text(whois_tab)


# PORT SCANNER TAB
port_tab = tk.Frame(notebook, bg="#0d0d0d")
notebook.add(port_tab, text="Port Scanner")

make_label(port_tab, "BASIC PORT SCANNER")
make_subtitle(port_tab, "Only scan systems you own or have permission to test")

port_target_entry = make_entry(port_tab)
port_target_entry.insert(0, "127.0.0.1")

port_list_entry = make_entry(port_tab)
port_list_entry.insert(0, "22,80,443")

make_button(port_tab, "Scan Ports", scan_ports, True).pack()

port_result = make_text(port_tab)


root.mainloop()