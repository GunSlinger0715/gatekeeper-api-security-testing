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
            findings.append({
                "finding": "Sensitive Data Exposure",
                "severity": "CRITICAL",
                "details": f"Sensitive field detected: {field}"
            })

    return findings

def check_info_leakage(response):
    findings = []

    headers = response.headers

    if "server" in headers:
        findings.append({
            "finding": "Information Leakage",
            "severity": "MEDIUM",
            "details": f"Server header exposed: {headers['server']}"
        })

    if "x-powered-by" in headers: 
        findings.append({
            "finding": "Information Leakage",
            "severity": "MEDIUM",
            "details": f"X-Powered-By header exposed: {headers['x-powered-by']}"
        })

    strength_issues = validate_header_strength(headers)

    if strength_issues:
        for issue in strength_issues:
            findings.append({
                "finding": "Weak Security Header Configuration",
                "severity": "LOW",
                "details": issue
        })

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
        "valid_headers": [],
        "findings": []
    }

    headers = response.headers

    for header, expected in REQUIRED_SECURITY_HEADERS.items():
        value = headers.get(header)

        if not value:

            results["missing_headers"].append(header)

            results["findings"].append({
                "finding": "Missing Security Header",
                "severity": "HIGH",
                "details": f"{header} header missing"
            })

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
    
        strength_issues = validate_header_strength(headers)

        for issue in strength_issues: 
            results["misconfigured_headers"].append(issue)


    return results        

def check_unauthorized_access(response, endpoint, protected_endpoints):

    findings = []
    secure_behavior = []

    if endpoint in protected_endpoints:  

            if response.status_code == 200:
                findings.append({
                    "finding": "Unauthorized Access Allowed",
                    "severity": "HIGH",
                    "details": "Protected endpoint accessible without authentication"
                })
            elif response.status_code in [401, 403]:

                secure_behavior.append({
                    "status": "PASS",
                    "details": "Protected endpoint correctly denied unauthorized access"
                })

                
    return findings, secure_behavior

# Sensitive field detection
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
        "Token": r"\b[A-Za-z0-9\-\._]{20,}\b",
        "Password Field": r'"password"\s*:\s*".*?"',
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, data_str)

        for match in matches:
            findings.append({
                "finding": f"{label} Exposure Detected",
                "severity": "HIGH",
                "details": f"{label} detected: {match}"
            })

            if label == "Token":
                issues = analyze_token(match)
                for issue in issues:
                    findings.append(f"⚠️ Token anomaly detected ({issue})")

    return findings

#Token Anomaly Detection
def analyze_token(token):
    issues = []

    # Length checks
    if len(token) < 20:
        issues.append({
            "finding": "Weak Token Structure",
            "severity": "MEDIUM",
            "details": "Token too short"
        })

    if len(token) > 500:
        issues.append({
            "finding": "Suspicious Token Length",
            "severity": "MEDIUM",
            "details": "Token unusually long"
        })

    # JWT structure check (header.payload.signature)
    parts = token.split(".")
    if len(parts) != 3:
        issues.append({
            "finding": "Invalid JWT Structure",
            "severity": "MEDIUM",
            "details": "Token does not follow JWT header.payload.signature format"
        })
def detect_and_analyze_tokens(data):
    findings = []

    token_pattern = re.compile(r'\b[A-Za-z0-9\-_\.]{20,}\b')

    for key, value in data.items():
        if not isinstance(value, str):
            continue

        matches = token_pattern.findall(value)

        for token in matches:
            issues = analyze_token(token)

            for issue in issues:
                issues["details"] += f" in field '{key}'"
                findings.append(issue)


    return issues

#Header Strength Validation
def validate_header_strength(headers):
    issues = []

    # --- Content-Security-Policy ---
    csp = headers.get("Content-Security-Policy")
    if csp:
        if "*" in csp:
            issues.append("[WARNING] CSP is too permissive (contains '*')")
        if "unsafe-inline" in csp:
            issues.append("[WARNING] CSP allows unsafe-inline (XSS risk)")

    # --- Strict-Transport-Security ---
    hsts = headers.get("Strict-Transport-Security")
    if hsts:
        if "includeSubDomains" not in hsts:
            issues.append("[WARNING] HSTS missing includeSubDomains")
        if "max-age" not in hsts:
            issues.append("[WARNING] HSTS missing max-age")

    # --- X-Frame-Options ---
    xfo = headers.get("X-Frame-Options")
    if xfo:
        if xfo not in ["DENY", "SAMEORIGIN"]:
            issues.append(f"[WARNING] Weak X-Frame-Options value: {xfo}")

    return issues

#Token Anomaly Detection

def detect_token_anomalies(data):
    findings = []

    # Regex for token-like strings (long random strings)
    token_pattern = re.compile(r'\b[A-Za-z0-9\-_]{20,}\b')

    for key, value in data.items():
        if not isinstance(value, str):
            continue

        matches = token_pattern.findall(value)

        for token in matches:
            
            # --- Length Check ---
            if len(token) > 100:
                findings.append({
                    "finding": "Suspicious Token Length",
                    "severity": "MEDIUM",
                    "details": f"Suspiciously long token detected in '{key}'"
             })

            # --- JWT Structure Check ---
            if token.count('.') == 2:
                parts = token.split('.')
                if all(len(part) > 0 for part in parts):
                    findings.append({
                        "finding": "JWT-Like Token Detected",
                        "severity": "LOW",
                        "details": f"JWT-like token detected in '{key}'"
            })

            # --- Weak / Likely False Positive ---
            if token.lower() in ["password", "username", "admin"]:
                continue

    return findings