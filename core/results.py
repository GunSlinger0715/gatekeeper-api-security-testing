# =========================================================
# SHARED RESULTS / EXECUTION STATE
# =========================================================

results_summary = {
    "tested": 0,
    "successful": 0,
    "failed": 0,
    "timeouts": 0,
    "scores": [],
    "risks": [],
    "info_exposures": 0,
    "missing_headers": 0,
    "sensitive_findings": 0
}

def print_operational_summary():

    print("\n" + "=" * 48)
    print("GATEKEEPER OPERATIONAL SUMMARY")
    print("=" * 48)

    print(f"\nEndpoints Tested:      {results_summary['tested']}")
    print(f"Successful Responses:  {results_summary['successful']}")
    print(f"Failed Responses:      {results_summary['failed']}")
    print(f"Timeouts Detected:     {results_summary['timeouts']}")

    if results_summary["scores"]:

        average_score = sum(results_summary["scores"]) // len(results_summary["scores"])

    else:
        average_score = 0

    print(f"\nAverage Security Score: {average_score}")

    if results_summary["risks"]:

        highest_risk = max(results_summary["risks"])

    else:
        highest_risk = "UNKNOWN"

    print(f"Highest Risk Level:    {highest_risk}")

    print(f"\nInformation Exposures: {results_summary['info_exposures']}")
    print(f"Missing Headers:       {results_summary['missing_headers']}")
    print(f"Sensitive Findings:    {results_summary['sensitive_findings']}")

    if results_summary["failed"] > 0:
        stability = "DEGRADED"
    else:
        stability = "STABLE"

    print(f"\nSystem Stability:      {stability}")

    print("=" * 48)

def create_finding(
        finding, 
        severity, 
        details, 
        why_it_matters=None, 
        recommended_actions=None,
        trust_level="unknown"
):
    return {
        "finding": finding,
        "severity": severity,
        "details": details,
        "why_it_matters": why_it_matters,
        "recommended_actions": recommended_actions or [],
        "trust_level": "unkown"
    }