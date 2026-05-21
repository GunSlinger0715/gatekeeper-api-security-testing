# =========================================================
# SHARED RESULTS / EXECUTION STATE
# =========================================================

results_summary = []


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