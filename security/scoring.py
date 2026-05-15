from config.colors import GREEN, YELLOW, RED, RESET 

# =========================================================
# SECURITY SCORING ENGINE
# =========================================================

#SEVERITY WEIGHTS
SEVERITY_WEIGHTS = {
    "INFO": 0,
    "LOW": 5,
    "MEDIUM": 15,
    "HIGH": 30,
    "CRITICAL": 50
}


def calculate_security_score(findings, leaks, header_results, sensitive):
    score = 100

    # Structured finding severity scoring
    for finding in sensitive:

        if isinstance(finding, dict):

            severity = finding.get("severity", "INFO")

            deduction = SEVERITY_WEIGHTS.get(severity, 0)

            score -= deduction

    # Data Exposure (HIGH)
    if findings:
        score -= len(findings) * 15

    #Info Leakage (MEDIUM)
    if leaks:
        score -= len(leaks) * 10
    
    # Token anomaly (EXTRA penalty)
    # Temporary legacy token anomaly handling
    # Will be normalized during security.py refactor
    if any(
        isinstance(f, dict) and "Token" in f.get("finding", "")
        for f in sensitive
    ):
        score -= 10

    # Missing Headers (MEDIUM)
    missing = header_results.get("missing_headers", [])
    score -= len(missing) * 5

    #Misconfigured headers (LOW)
    misconfigured = header_results.get("misconfigured_headers", [])
    score -= len(misconfigured) * 3

    return max(score, 0)


def get_risk_level(score):
    if score >= 90:
        return "LOW RISK"

    elif score >= 70:
        return "MEDIUM RISK"

    elif score >= 40:
        return "HIGH RISK"

    return "CRITICAL"

def get_risk_color(risk):
    if risk == "HIGH RISK":
        return RED
    elif risk == "MEDIUM RISK":
        return YELLOW
    elif risk == "LOW RISK":
        return GREEN
    return RESET