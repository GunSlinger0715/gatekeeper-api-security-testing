# imports
import re


# utils/security.py

def check_data_exposure(response):
    findings = []

    # Safely get response body
    try:
        data = response.json()
        data_str = str(data).lower()
    except Exception:
        data_str = ""

    return findings

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

    return findings

def check_info_leakage(response):
    findings = []

    headers = response.headers

    if "server" in headers:
        findings.append(f"Header exposed: Server = {headers['server']}")

    if "x-powered-by" in headers: 
        findings.append(f"Header exposed: X-Powered-By = {headers['x-powered-by']}")

    return findings

REQUIRED_SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": ["DENY", "SAMEORIGIN"],
    "Content-Security-Policy": None,
    "Referrer-Policy": None,
    "Permissions-Policy": None
}

def check_header_integrity(response):
    results = {
        "missing_headers": [],
        "misconfigured_headers": [],
        "valid_headers": []
    }

    headers = response.headers

    for header, expected in REQUIRED_SECURITY_HEADERS.items():
        value = headers.get(header)

        if not value:
            results["missing_headers"].append(header)
            continue

        if expected:
            if isinstance(expected, list):
                if not any(opt in value for opt in expected):
                    results["misconfigured_headers"].append((header, value))
                else:
                    results["valid_headers"].append(header)
            else:
                if expected not in value:
                    results["misconfigured_headers"].append((header, value))
                else:
                    results["valid_headers"].append(header)
        else:
            results["valid_headers"].append(header)

    return results

#Sensittive field detection
def check_sensitive_fields(response):
    findings = []

    try: 
        data = response.json()
    except Exception:
            return findings #Not JSON, skip
    
    data_str = str(data)

    patterns = {
        "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "Token": r"[A-Za-z0-9\-\._]{12,}",
        "Password Field": r'"password"\s*:\s*".*?"',
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, data_str)

        for match in matches:
            findings.append(f"{label} detected: {match}")

            if label == "Token":
                issues = analyze_token(match)
                for issue in issues:
                    findings.append(f"⚠️ Token anomaly: {issue}")

    return findings

#Token Anomaly Detection
def analyze_token(token):
    issues = []

    # Length checks
    if len(token) < 20:
        issues.append("Token too short")

    if len(token) > 500:
        issues.append("Token unusually long")

    # JWT structure check (header.payload.signature)
    parts = token.split(".")
    if len(parts) != 3:
        issues.append("Invalid JWT structure")

    return issues