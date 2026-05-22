# =========================================================
# Adaptive Response Handling
#
# Purpose:
# Safely classify and process API responses
# without assuming all responses are JSON.
#
# Future Goals:
# - Content-Type awareness
# - Adaptive parser routing
# - Response anomaly detection
# - Heimdall interpretation support
# - Monolith intelligence enrichment
# =========================================================


def detect_content_type(response):

    if response is None:

        print("[WARNING] No response received")

        return "unknown"

    content_type = response.headers.get("Content-Type", "").lower()

    if "application/json" in content_type:
        return "json"

    elif "text/html" in content_type:
        return "html"

    elif "text/plain" in content_type:
        return "text"

    elif "application/xml" in content_type:
        return "xml"

    else:
        return "unknown"