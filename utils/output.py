import json
from core import context
from utils.security import (
    check_data_exposure,
    check_info_leakage,
    check_header_integrity,
    check_sensitive_fields, 
    check_unauthorized_access
)
from security.scoring import (
    calculate_security_score,
    get_risk_level,
    get_risk_color
)

from core.results import results_summary, print_operational_summary
from core.lifecycle import ExecutionLifecycle

from config.colors import GREEN, YELLOW, RED, RESET
from reporting.export import export_results_to_json
from core.context import ExecutionContext
from core.history import (
    store_execution_context,
    print_execution_history,
    compare_last_execution,
    export_execution_history
)
# =========================================================
# RESULT RENDERING / OUTPUT DISPLAY
# =========================================================

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

#Structured Fingins Rendering
def print_structured_findings(findings):
    for finding in findings: 

        if isinstance(finding, dict):
            print(f" - [{finding['severity']}] {finding['details']}")
        
        else: 
            print(f" - {finding}")

# Exposure Analysis Rendering
def print_data_exposure(findings, endpoint):
    if findings:
        print(f"\n\033[93m[SECURITY FINDINGS] {endpoint} - Data Exposure Analysis:\033[0m")
        print_structured_findings(findings)
        print("-" * 40)


def print_info_leakage(leaks, endpoint):
    if leaks:
        print(f"\n\033[93m[SECURITY FINDINGS] {endpoint} - Information Exposure Analysis:\033[0m")
        print_structured_findings(leaks)
        print("-" * 40)

# Header Analysis Rendering
def print_header_integrity(results, endpoint):
    if results["missing_headers"]:
        print(f"\n\033[93m[SECURITY FINDINGS] {endpoint} - Missing Security Headers:\033[0m")
        for h in results["missing_headers"]:
            print(f"  - {h}")

    if results["misconfigured_headers"]:
        print(f"\n\033[93m[SECURITY FINDINGS] {endpoint} - Misconfigured Headers:\033[0m")
        for issue in results["misconfigured_headers"]:

            header = issue["header"]
            value = issue["observed_value"]

            print(f" - {header}: {value}")

    if results["valid_headers"]:
        print("\n\033[92m[PASS] Valid Security Headers:\033[0m")
        for h in results["valid_headers"]:
            print(f"  - {h}")

        print("-" * 40)

# Security Score Rendering
def print_security_score(score, endpoint):

    risk = get_risk_level(score)

    color = get_risk_color(risk)

    print(f"\n{color}[SECURITY SCORE] {endpoint} → {score}/100 ({risk}){RESET}")

# =========================================================
# SECURITY ANALYSIS ORCHESTRATION
# =========================================================

with open("config/protected_endpoints.json", "r") as f:
    protected_endpoints = json.load(f)

def run_security_checks(response, endpoint):

    lifecycle = ExecutionLifecycle()
    context = ExecutionContext(endpoint)
    lifecycle.enter_phase("RESPONSE_VALIDATION")
    context.set_phase(lifecycle.get_current_phase())

    lifecycle.enter_phase("SECURITY_ANALYSIS")
    context.set_phase(lifecycle.get_current_phase())
    findings, observations = check_data_exposure(response)

    context.add_findings(findings)

    for observation in observations: 
        context.add_observation(observation)

    print_data_exposure(findings, endpoint)

    leaks, observations = check_info_leakage(response)
    context.add_findings(leaks)
    
    for observation in observations:
        context.add_observation(observation)
    print_info_leakage(leaks, endpoint)

    header_results = check_header_integrity(response)
    context.add_findings(header_results["findings"])

    for observation in header_results["observations"]:
        context.add_observation(observation)
    
    print_header_integrity(header_results, endpoint)

    unauthorized, secure_behavior, observations = check_unauthorized_access(
        response,
        endpoint,
        protected_endpoints
    )

    for observation in observations: 
        context.add_observation(observation)

    if unauthorized:

        context.add_findings(unauthorized)

        print("\n\033[91m[FAIL] Unauthorized Access Detected:\033[0m")

        for finding in unauthorized:
            print(f" - [{finding['severity']}] {finding['details']}")

        print("-" * 40)

    if secure_behavior:

        print("\n\033[92m[PASS] Secure Authorization Behavior Detected:\033[0m")

        for behavior in secure_behavior:
            print(f" - {behavior['details']}")

        print("-" * 40)

    # ----------------------------
    # Sensitive Field Detection
    # ----------------------------
    sensitive = check_sensitive_fields(response)
    context.add_findings(sensitive)

    # Sensitive Findings Rendering
    print_sensitive_findings(sensitive, endpoint)

    lifecycle.enter_phase("OPERATIONAL_CLASSIFICATION")
    context.set_phase(lifecycle.get_current_phase())
    score = calculate_security_score(findings, leaks, header_results, sensitive)
    context.set_score(score)
    print_security_score(score, endpoint)
    risk = get_risk_level(score)

    context.set_risk(risk)

    print(f"\n[DEBUG] Centralized Findings Count: {len(context.findings)}")
    
    exposure_findings = findings
    header_findings = header_results.get("findings", [])

    lifecycle.enter_phase("TELEMETRY_AGGREGATION")
    context.set_phase(lifecycle.get_current_phase())
    results_summary["tested"] += 1

    if context.score >= 70:
        results_summary["successful"] += 1
    else:
        results_summary["failed"] += 1

    if score >= 70:
        context.set_stability("STABLE")
    else:
        context.set_stability("DEGRADED")

    results_summary["scores"].append(score)
    results_summary["risks"].append(context.risk)

    results_summary["info_exposures"] += len(exposure_findings)
    results_summary["missing_headers"] += len(header_findings)
    results_summary["sensitive_findings"] += len(sensitive)

    lifecycle.enter_phase("FINAL_RENDERING")
    context.set_phase(lifecycle.get_current_phase())

    print("\n[DEBUG] Serialized Execution Context:")

    serialized = context.to_dict()

    print(f" Endpoint: {serialized['endpoint']}")
    print(f" Score: {serialized['score']}")
    print(f" Risk: {serialized['risk']}")
    print(f" Current Phase: {serialized['current_phase']}")
    print(f" Findings Count: {len(serialized['findings'])}")
    store_execution_context(context)

    print("\n[DEBUG] Execution Context Stored In History")

    print_execution_history()

    compare_last_execution()

    export_execution_history()
    print("\n[DEBUG] Execution History Exported to JSON")

    lifecycle.print_completed_phases()
    
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



#Sensitive Field Output

def print_sensitive_findings(findings, endpoint):
    if findings:
        print(f"\n\033[93m[SECURITY FINDINGS] {endpoint} - Sensitive Field Analysis:\033[0m")
        print_structured_findings(findings)
        print("-" * 40)