# utils/security.py

def check_data_exposure(response):
    findings = []

    # Safely get response body
    try:
        data = response.json()
        data_str = str(data).lower()
    except Exception:
        data_str = ""

    # 🔐 Sensitive fields (v1 scope)
    sensitive_fields = [
        "password",
        "password_hash",
        "is_admin",
        "internal_notes",
        "created_by_ip",
        "token"
    ]

    # Scan for sensitive fields
    for field in sensitive_fields:
        if field in data_str:
            findings.append(f"Sensitive field detected: {field}")

def check_info_leakage(response):
    findings = []

    headers = response.headers

    if "server" in headers:
        findings.append(f"Header exposed: Server = {headers['server']}")

    if "x-powered-by" in headers: 
        findings.append(f"Header exposed: X-Powered-By = {headers['x-powered-by']}")

    return findings