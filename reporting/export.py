import json

from core.results import results_summary

# =========================================================
# RESULT EXPORTING / PERSISTENCE
# =========================================================

#Output to JSON
def export_results_to_json(filename="gatekeeper_results.json"):
    with open(filename, "w") as f:
        json.dump(results_summary, f, indent=4)

    print(f"\n📁 Results exported to {filename}")