# =========================================================
# SHARED RESULTS / EXECUTION STATE
# =========================================================

results_summary = []


def create_finding(finding, severity, details): 
    return{
        "finding": finding,
        "severity": severity,
        "details": details
    }