# Cyber Toolkit

Cyber Toolkit is a Python-based cybersecurity desktop application built with Tkinter.  
The toolkit provides multiple security analysis utilities inside a modern desktop GUI 
designed for students, beginners, and cybersecurity enthusiasts.

Note: Subdomain enumeration uses public certificate transparency logs. Some domains may fail temporarily if the public source is slow, rate-limited, or unavailable.

## Features

- Hash Identifier
- TXT Hash Upload Support
- HTTP Security Header Scanner
- Password Breach Checker
- WHOIS Lookup
- DNS Lookup
- Port Scanner
- PDF Export Support
- Local Scan History
- Multi-threaded Scanning
- macOS Desktop App Bundle
- CVE Vulnerability Search
- Passive Subdomain Enumeration
- Advanced Nmap Scanner
- Rule-Based Security Recommendations
- Nmap PDF Export
- Service Version Detection


## Technologies Used

- Python
- Tkinter
- Requests
- Socket
- ReportLab
- python-whois
- dnspython
- hashlib
- threading

## Screenshots

## Hash Identifier
![Hash](screenshots/hash.png)

## HTTP Headers Scanner
![Headers](screenshots/headers.png)

## Security Recommendations
![Recommendations](screenshots/recommendation.png)

## Password Breach Checker
![Breach](screenshots/breach.png)

## WHOIS Lookup
![WHOIS](screenshots/whois.png)

## DNS Lookup
![DNS](screenshots/dns.png)

## Port Scanner
![Ports](screenshots/ports.png)

## CVE Search
![CVE Search](screenshots/CVEsearch.png)

## Passive Subdomain Enumeration
![Subdomain Enumeration](screenshots/subdomain_enum.png)

## Nmap Recommendations & PDF Export
![Nmap Advanced](screenshots/Nmap2.png)

### Scan History
![History](screenshots/history.png)


## Installation

```bash

git clone https://github.com/AhmedSh7/Cyber-Toolkit.git
cd Cyber-Toolkit

pip install -r requirements.txt
python main.py
```

## Build macOS App

```bash
pyinstaller "Cyber Toolkit.spec"
```

## Author

Ahmed Shammout

- GitHub: https://github.com/AhmedSh7
- LinkedIn: https://www.linkedin.com/in/ahmed-shammout/
- Cybersecurity Graduate

