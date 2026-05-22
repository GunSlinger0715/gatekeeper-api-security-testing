# =========================================================
# EXECUTION HISTORY MANAGEMENT ENGINE
#
# Purpose:
# Persist and manage historical execution telemetry for
# GateKeeper orchestration workflows.
#
# Responsibilities:
# - Store serialized execution contexts
# - Maintain execution telemetry history
# - Support future historical analysis
# - Enable execution replay capabilities
# - Provide orchestration memory persistence
#
# Future Expansion:
# - Historical anomaly detection
# - Execution baselining
# - Telemetry correlation analytics
# - Heimdall visualization timelines
# - Adaptive orchestration intelligence
#
# Engineering Philosophy:
# From Execution Intelligence to Operational Memory.
# =========================================================

execution_history = []

def store_execution_context(context):

    execution_history.append(context.to_dict())

def print_execution_history():

    print("\n========== EXECUTION HISTORY ==========")

    for index, execution in enumerate(execution_history, start=1):

        print(f"\nExecution #{index}")

        print(f" Endpoint: {execution['endpoint']}")
        print(f" Score: {execution['score']}")
        print(f" Risk: {execution['risk']}")
        print(f" Phase: {execution['current_phase']}")
        print(f" Findings: {len(execution['findings'])}")

def compare_last_execution():

    if len(execution_history) < 2:
        return
    
    previous = execution_history[-2]
    current = execution_history[-1]

    print("\n========== EXECUTION DELTA ==========")

    score_delta = current["score"] - previous["score"]

    findings_delta = (
        len(current["findings"])-
        len(previous["findings"])
    )

    print(f" Score Delta: {score_delta}")

    print(f" Findings Delta: {findings_delta}")

    previous_stability = previous.get("stability")
    current_stability = current.get("stability")

    print(f" Stability Transition: {previous_stability} -> {current_stability}")
    