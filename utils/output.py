import json
from utils.security import (
    check_data_exposure,
    check_info_leakage,
    check_header_integrity,
    check_sensitive_fields  
)

# Risk level coloring
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"



from utils.security import (
    check_data_exposure,
    check_info_leakage,
    check_header_integrity
)



# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

results_summary =[]


def print_result(endpoint, method, status_code, expected, passed):
    if passed:
        print(f"{GREEN}[PASS]{RESET} {method} {endpoint} → {status_code} | {get_status_message(status_code)}")
    else:
        print(f"{RED}[FAIL]{RESET} {method} {endpoint} → {status_code}")
        print(f"{RED}       Expected: {expected}{RESET}")
        print(f"{RED}       Reason: {get_status_message(status_code)}{RESET}")


def get_status_message(status_code):
    messages = {
        200: "OK - Request successful",
        201: "Created - Resource created successfully",
        400: "Bad Request - Invalid input",
        401: "Unauthorized - Authentication required",
        403: "Forbidden - Access denied",
        404: "Not Found - Resource does not exist",
        500: "Server Error - Internal issue"
    }
    return messages.get(status_code, "Unknown response")


def print_data_exposure(findings, endpoint):
    if findings:
        print(f"\n\033[93m[WARNING] {endpoint} - Potential data exposure detected:\033[0m")
        for f in findings:
            print(f"  - {f}")
        print("-" * 40)


def print_info_leakage(leaks, endpoint):
    if leaks:
        print(f"\n\033[93m[WARNING] {endpoint} - Potential information leakage detected:\033[0m")
        for l in leaks:
            print(f"  - {l}")
        print("-" * 40)


def print_header_integrity(results):
    if results["missing_headers"]:
        print("\n\033[91m[FAIL] Missing Security Headers:\033[0m")
        for h in results["missing_headers"]:
            print(f"  - {h}")

    if results["misconfigured_headers"]:
        print("\n\033[93m[WARN] Misconfigured Headers:\033[0m")
        for h, val in results["misconfigured_headers"]:
            print(f"  - {h}: {val}")

    if results["valid_headers"]:
        print("\n\033[92m[PASS] Valid Security Headers:\033[0m")
        for h in results["valid_headers"]:
            print(f"  - {h}")

    print("-" * 40)



def calculate_security_score(findings, leaks, header_results, sensitive):
    score = 100

    # Data Exposure (HIGH)
    if findings:
        score -= len(findings) * 15

    #Info Leakage (MEDIUM)
    if leaks:
        score -= len(leaks) * 10
    
    #Sensitive data (VERY HIGH)
    if sensitive: 
        score -= len(sensitive) * 20
    
    # Token anomaly (EXTRA penalty)
    if any ("Token anomaly" in f for f in sensitive):
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
    elif score >= 50:
        return "HIGH RISK"
    else:
        return "CRITICAL RISK"


def print_security_score(score, endpoint):
    risk = get_risk_level(score)

    if score >= 90:
        color = "\033[92m"
    elif score >= 70:
        color = "\033[93m"
    else:
        color = "\033[91m"

    print(f"\n{color}[SECURITY SCORE] {endpoint} → {score}/100 ({risk})\033[0m")


def run_security_checks(response, endpoint):
    findings = check_data_exposure(response)
    print_data_exposure(findings, endpoint)

    leaks = check_info_leakage(response)
    print_info_leakage(leaks, endpoint)

    header_results = check_header_integrity(response)
    print_header_integrity(header_results)

    # ----------------------------
    # Sensitive Field Detection
    # ----------------------------
    sensitive = check_sensitive_fields(response)
    print_sensitive_findings(sensitive, endpoint)

    score = calculate_security_score(findings, leaks, header_results, sensitive)
    print_security_score(score, endpoint)

    results_summary.append({
        "method": endpoint.split()[0],
        "endpoint": endpoint.split()[1],
        "score": score,
        "risk": get_risk_level(score)
    })

def get_risk_color(risk):
    if risk == "HIGH RISK":
        return RED
    elif risk == "MEDIUM RISK":
        return YELLOW
    elif risk == "LOW RISK":
        return GREEN
    return RESET    

def print_summary():
    print("\n\n========== SECURITY SUMMARY ==========")
    print(f"{'Method':<8}{'Endpoint':<25}{'Score':<8}{'Risk'}")
    print("-" * 60)

    # Risk order
    risk_order = {
        "HIGH RISK": 0, 
        "MEDIUM RISK": 1, 
        "LOW RISK": 2
    }

    sorted_results = sorted(
    results_summary,
    key=lambda x: x["score"]
)
    for result in sorted_results:
        color = get_risk_color(result["risk"])
        print(f"{result['method']:<10}{result['endpoint']:<20}{result['score']:<10}{color}{result['risk']}{RESET}")
    export_results_to_json()    


#Output to JSON
def export_results_to_json(filename="gatekeeper_results.json"):
    with open(filename, "w") as f:
        json.dump(results_summary, f, indent=4)

    print(f"\n📁 Results exported to {filename}")

#Sensitive Field Output
YELLOW = "\033[93m"

def print_sensitive_findings(findings, endpoint):
    if findings:
        print(f"\n{YELLOW}[WARNING] {endpoint} - Sensitive data detected:\033[0m")
        for f in findings:
            print(f" - {f}")
        print("-" * 40)   

