def get_recommendations(tool_name, result_text):
    recommendations = []

    text = result_text.lower()

    if "content-security-policy" in text and "missing" in text:
        recommendations.append(
            "Add a Content-Security-Policy header to help reduce XSS and injection risks."
        )

    if "strict-transport-security" in text and "missing" in text:
        recommendations.append(
            "Add HTTP Strict Transport Security to force browsers to use HTTPS."
        )

    if "x-frame-options" in text and "missing" in text:
        recommendations.append(
            "Add X-Frame-Options or CSP frame-ancestors to help prevent clickjacking."
        )

    if "x-content-type-options" in text and "missing" in text:
        recommendations.append(
            "Add X-Content-Type-Options: nosniff to reduce MIME-sniffing risks."
        )

    if "telnet" in text or "port 23" in text:
        recommendations.append(
            "Disable Telnet if possible and use SSH instead because Telnet sends data in plaintext."
        )

    if "ftp" in text or "port 21" in text:
        recommendations.append(
            "Avoid plain FTP and use SFTP or FTPS for encrypted file transfer."
        )

    if "critical" in text:
        recommendations.append(
            "Prioritize critical vulnerabilities immediately and review vendor patches or mitigations."
        )

    if "high" in text:
        recommendations.append(
            "Review high-severity findings soon and apply security updates where available."
        )

    if not recommendations:
        recommendations.append(
            "No specific recommendation found. Review the scan results manually and follow security best practices."
        )

    output = "\n\nSecurity Recommendations:\n"
    output += "-" * 30 + "\n"

    for rec in recommendations:
        output += f"- {rec}\n"

    return output