# imports
import re

from core.observation_factory import create_observation


# utils/security.py

# =========================================================
# DATA EXPOSURE ANALYSIS
# =========================================================

def check_data_exposure(response):
    findings = []
    observations = []

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
            observations.append(
                create_observation(
                    observation_type="SENSITIVE_FIELD_EXPOSED",
                    details=f"Sensitive field detected: {field}",
                    confidence=100,
                    source="DATA_EXPOSURE_ANALYZER"
                )
            )

    return findings, observations

# =========================================================
# INFORMATION LEAKAGE ANALYSIS
# =========================================================

def check_info_leakage(response):
    findings = []
    observations = []

    headers = response.headers

    if "server" in headers:
        findings.append({
            "finding": "Information Leakage",
            "severity": "MEDIUM",
            "details": f"Server header exposed: {headers['server']}"
        })

        observations.append(
            create_observation(
                observation_type="SERVER_HEADER_EXPOSED",
                details=f"Server header exposed: {headers['server']}",
                confidence=100,
                source="HEADER_ANALYZER"
            )
        )

    if "x-powered-by" in headers: 
        findings.append({
            "finding": "Information Leakage",
            "severity": "MEDIUM",
            "details": f"X-Powered-By header exposed: {headers['x-powered-by']}"
        })

    return findings, observations

# =========================================================
# HEADER SECURITY ANALYSIS
# =========================================================

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
        "findings": [], 
        "observations": []
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

            results["observations"].append(
                create_observation(
                    observation_type="MISSING_SECURITY_HEADER",
                    details=f"{header} header missing",
                    confidence=100,
                    source="HEADER_INTEGRITY_ANALYZER"
                )
            )

            continue

    if expected: 

        if isinstance(expected, list):

            if not(opt in value for opt in expected):

                results["misconfigured_headers"].append({
                    "header": header, 
                    "observed_value": value, 
                    "issue": "Misconfigured Header"
                })

            else: 
                results["valid_headers"].append(header)

        else:

            if expected not in value: 

                results["misconfigured_headers"].append({
                    "header": header, 
                    "observed_value": value, 
                    "issue": "Misconfigured Header"
                })
            else: 
                results["valid_headers"].append(header)

    else: 
        results["valid_headers"].append(header)

    # ------------------------------------
    # Header Strength Validation
    # ------------------------------------
    strength_issues, strength_observations = validate_header_strength(headers)

    results["findings"].extend(strength_issues)
    results["observations"].extend(strength_observations) 
    
    return results    

# =========================================================
# AUTHORIZATION ANALYSIS
# =========================================================    

def check_unauthorized_access(response, endpoint, protected_endpoints):

    findings = []
    secure_behavior = []
    observations = []

    if endpoint in protected_endpoints:  

            if response.status_code == 200:
                findings.append({
                    "finding": "Unauthorized Access Allowed",
                    "severity": "HIGH",
                    "details": "Protected endpoint accessible without authentication"
                })

                observations.append(
                    create_observation(
                        observation_type="UNAUTHORIZED_ACCESS_ALLOWED",
                        details="Protected endpoint accessible without authentication",
                        confidence=100,
                        source="AUTHORIZATION_ANALYZER"
                    )
                )
            elif response.status_code in [401, 403]:

                secure_behavior.append({
                    "status": "PASS",
                    "details": "Protected endpoint correctly denied unauthorized access"
                })
                observations.append(
                    create_observation(
                        observation_type="AUTHORIZATION_ENFORCED",
                        details="Protected endpoint correctly denied unauthorized access",
                        confidence=100,
                        source="AUTHORIZATION_ANALYZER"
                    )
                )

                
    return findings, secure_behavior, observations

# Sensitive field detection
def check_sensitive_fields(response):
    findings = []
    observations = []

    try: 
        data = response.json()
    except Exception:
            return findings, observations #Not JSON, skip
    
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

            observations.append(
                create_observation(
                    observation_type=f"{label.upper().replace(' ', '_')}_EXPOSED",
                    details=f"{label} detected: {match}",
                    confidence=100,
                    source="SENSITIVE_FIELD_ANALYZER"
                )
            )

            if label == "Token": 
                issues, token_observations = analyze_token(match)

                for issue in issues: 
                    findings.append(issue)

                for observation in token_observations: 
                    observations.append(observation)
    return findings, observations 

#Token Anomaly Detection
def analyze_token(token):
    issues = []
    observations = []

    # Length checks
    if len(token) < 20:
        issues.append({
            "finding": "Weak Token Structure",
            "severity": "MEDIUM",
            "details": "Token too short"
        })

        observations.append(
            create_observation(
                observation_type="WEAK_TOKEN_STRUCTURE",
                details="Token too short", 
                confidence=100,
                source="TOKEN_ANALYZER"
            )
        )

    if len(token) > 500:
        issues.append({
            "finding": "Suspicious Token Length",
            "severity": "MEDIUM",
            "details": "Token unusually long"
        })

        observations.append(
            create_observation(
                observation_type="SUSPICIOUS_TOKEN_LENGTH",
                details="Token unusually long",
                confidence=100,
                source="TOKEN_ANALYZER"
            )
        )

    # JWT structure check (header.payload.signature)
    parts = token.split(".")
    if len(parts) != 3:
        issues.append({
            "finding": "Invalid JWT Structure",
            "severity": "MEDIUM",
            "details": "Token does not follow JWT header.payload.signature format"
        })

        observations.append(
            create_observation(
                observation_type="INVALID_JWT_STRUCTURE",
                details="Token does not follow JWT header.payload.signature format",
                confidence=100,
                source="TOKEN_ANALYZER"
            )
        )

    return issues, observations

def detect_and_analyze_tokens(data):
    findings = []

    token_pattern = re.compile(r'\b[A-Za-z0-9\-_\.]{20,}\b')

    for key, value in data.items():
        if not isinstance(value, str):
            continue

        matches = token_pattern.findall(value)

        for token in matches:
            issues, _ = analyze_token(token)

            for issue in issues:
                issue["details"] += f" in field '{key}'"
                findings.append(issue)


    return findings

#Header Strength Validation
def validate_header_strength(headers):
    issues = []
    observations = []

    # --- Content-Security-Policy ---
    csp = headers.get("Content-Security-Policy")
    if csp:
        if "*" in csp:
            issues.append({
                "finding": "Weak Content Security Policy",
                "severity": "HIGH",
                "details": "CSP is too permissive (contains'*')"
            })

            observations.append(
                create_observation(
                    observation_type="WEAK_CSP_WILDCARD",
                    details="CSP is too permissive (contains '*')",
                    confidence=100,
                    source="HEADER_STRENGTH_ANALYZER"
                )
            )

        if "unsafe-inline" in csp:
            issues.append({
                "finding": "Weak Content Security Policy",
                "severity": "HIGH",
                "details": "CSP allows unsafe-inline (XSS risk)"
            })

            observations.append(
                create_observation(
                    observation_type="UNSAFE_INLINE_CSP",
                    details="CSP allows unsafe-inline (XSS risk)",
                    confidence=100,
                    source="HEADER_STRENGTH_ANALYZER"
                )
            )

    # --- Strict-Transport-Security ---
    hsts = headers.get("Strict-Transport-Security")
    if hsts:
        if "includeSubDomains" not in hsts:
            issues.append({
                "finding": "Weak HTTP Strict Transport Security",
                "severity": "MEDIUM",
                "details": "HSTS missing includeSubDomains"
            })

            observations.append(
                create_observation(
                    observation_type="HSTS_MISSING_INCLUDE_SUBDOMAINS",
                    details="HSTS missing includeSubDomains",
                    confidence=100,
                    source="HEADER_STRENGTH_ANALYZER"
                )
            )

        if "max-age" not in hsts:
            issues.append({
                "finding": "Weak HTTP Strict Transport Security",
                "severity": "MEDIUM",
                "details": "HSTS missing max-age"
            })

            observations.append(
                create_observation(
                    observation_type="HSTS_MISSING_MAX_AGE",
                    details="HSTS missing max-age",
                    confidence=100,
                    source="HEADER_STRENGTH_ANALYZER"
                )
            )

    # --- X-Frame-Options ---
    xfo = headers.get("X-Frame-Options")
    if xfo:
        if xfo not in ["DENY", "SAMEORIGIN"]:
            issues.append({
                "finding": "Weak X-Frame-Options Configuration",
                "severity": "MEDIUM",
                "details": f"Weak X-Frame-Options value detected: {xfo}"
            })
            
            observations.append(
                create_observation(
                    observation_type="WEAK_X_FRAME_OPTIONS",
                    details=f"Weak X-Frame-Options value detected: {xfo}",
                    confidence=100,
                    source="HEADER_STRENGTH_ANALYZER"
                )
            )

    return issues, observations