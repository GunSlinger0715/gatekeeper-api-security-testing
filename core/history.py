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
import os 
import json 
from datetime import datetime

EXPECTED_FINDINGS_BASELINE = 5
EXECUTION_CONTEXT = "manual_test"


execution_history = []

def store_execution_context(context):

    execution_history.append(context.to_dict())

def export_execution_history():
    os.makedirs("telemetry", exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = f"telemetry/execution_history_{timestamp}.json"
    with open(filename, "w") as file:
        total_findings = sum(
            len(execution["findings"])
            for execution in execution_history
        )

        stable_executions = sum(
            1 for execution in execution_history
            if execution.get("stability") == "STABLE"
            
        )

        degraded_executions = sum(
            1 for execution in execution_history
            if execution["stability"] == "DEGRADED"
        )

        telemetry_export = {
            "telemetry_summary": "1.0",

            "generatd_at": timestamp,
            "execution_context": EXECUTION_CONTEXT,

            "summary":{
                "total_executions": len(execution_history),
                "total_findings": total_findings,
                "stable_executions": stable_executions,
                "degraded_executions": degraded_executions

            },
            "execution_history": execution_history
        }
        json.dump(telemetry_export, file, indent=4)
    print(f"\n[DEBUG] Telemetry Export Created: {filename}")

def update_telemetry_index(
    filename,
    total_findings,
    telemetry_health
):

    index_file = "telemetry/execution_index.json"

    telemetry_entry = {

        "file": filename,

        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "findings": total_findings,

        "health": telemetry_health,

        "stability": execution_history[-1]["stability"]
    }

    try:

        with open(index_file, "r") as file:

            telemetry_index = json.load(file)

    except FileNotFoundError:

        telemetry_index = []

    telemetry_index.append(telemetry_entry)

    with open(index_file, "w") as file:

        json.dump(
            telemetry_index,
            file,
            indent=4
        )

    print(
        f"\n[DEBUG] Telemetry Index Updated: "
        f"{index_file}"
    )

def telemetry_archive_count():
    telemetry_files = [
        file for file in os.lstdir("telemetry")
        if file.startswith("execution_history_")
    ]     
    print(
        f"\n[DEBUG] Telemetry Archive Count: "
        f"{len(telemetry_files)}"
    )

def analyze_findings_trend():
    telemetry_files = sorted(

        [
            file for file in os.listdir("telemetry")

            if file.startswith("execution_history_")
        ]

    )

    if len(telemetry_files) < 2:

        print("\n[DEBUG] Not enough telemetry archives for trend analysis.")

        return

    latest_file = telemetry_files[-1]

    previous_file = telemetry_files[-2]

    with open(f"telemetry/{latest_file}", "r") as file:

        latest_data = json.load(file)

    with open(f"telemetry/{previous_file}", "r") as file:

        previous_data = json.load(file)

    latest_findings = latest_data["summary"]["total_findings"]

    previous_findings = previous_data["summary"]["total_findings"]

    detect_findings_anomaly(
        previous_findings, 
        latest_findings
    )

    print("\n========== FINDINGS TREND ANALYSIS ==========")

    if latest_findings > previous_findings:

        print(" Findings Trend: DEGRADING")

    elif latest_findings < previous_findings:

        print(" Findings Trend: IMPROVING")

    else:

        print(" Findings Trend: STABLE")

def analyze_baseline_deviation(
        current_findings
):
    print(
         "\n========== BASELINE ANALYSIS =========="
    )
    if current_findings > EXPECTED_FINDINGS_BASELINE:

        deviation = (
            current_findings
            - EXPECTED_FINDINGS_BASELINE
        )
        print(
            f" Opertaional posture exceeds "
            f"baseline by {deviation} findings."
        )
    else:
        
        print(
            " Operational posture within "
            "expected baseline."
        )

def generate_telemetry_tags(
    telemetry_health,
    stability,
    anomaly_detected,
    baseline_exceeded
):

    tags = []

    tags.append(
        telemetry_health.lower()
    )

    tags.append(
        stability.lower()
    )

    if anomaly_detected:

        tags.append("anomaly")

    if baseline_exceeded:

        tags.append("baseline_exceeded")

    return tags

def classify_telemetry_priority(
    total_findings,
    telemetry_health,
    anomaly_detected
):

    if (
        telemetry_health == "CRITICAL"
        or anomaly_detected
        or total_findings >= 15
    ):

        return "HIGH"

    elif (
        telemetry_health == "WARNING"
        or total_findings > EXPECTED_FINDINGS_BASELINE
    ):

        return "MEDIUM"

    return "LOW"

def classify_telemetry_age():

    current_hour = datetime.now().hour

    if current_hour < 24:

        return "recent"

    elif current_hour < 48:

        return "aging"

    return "historical"

def detect_state_transition(
    previous_state,
    current_state,
    category
):

    if previous_state != current_state:

        print(
            f"\n[TRANSITION] {category} changed:"
        )

        print(
            f" {previous_state} → {current_state}"
        )

        return True

    return False

def classify_transition_direction(
    previous_state,
    current_state
):

    state_order = {

        "HEALTHY": 1,
        "WARNING": 2,
        "CRITICAL": 3
    }

    previous_value = state_order.get(
        previous_state,
        0
    )

    current_value = state_order.get(
        current_state,
        0
    )

    if current_value > previous_value:

        return "ESCALATING"

    elif current_value < previous_value:

        return "IMPROVING"

    return "UNCHANGED"

def report_transition_direction(
    previous_state,
    current_state,
    category
):

    direction = classify_transition_direction(
        previous_state,
        current_state
    )

    print(
        f" Direction: {direction}"
    )

    if direction == "ESCALATING":

        print(
            f" [WARNING] {category} escalation detected."
        )

    elif direction == "IMPROVING":

        print(
            f" [INFO] {category} recovery detected."
        )

def generate_operational_summary(

    telemetry_health,
    telemetry_priority,
    findings_trend,
    anomaly_detected,
    baseline_exceeded,
    execution_context

):

    print(
        "\n========== OPERATIONAL SUMMARY =========="
    )

    print(
        f" Health Status: "
        f"{telemetry_health}"
    )

    print(
        f" Priority Level: "
        f"{telemetry_priority}"
    )

    print(
        f" Findings Trend: "
        f"{findings_trend}"
    )

    print(
        f" Anomaly Detected: "
        f"{anomaly_detected}"
    )

    print(
        f" Baseline Exceeded: "
        f"{baseline_exceeded}"
    )

    print(
        f" Execution Context: "
        f"{execution_context}"
    )

def classify_telemetry_health(total_findings):

    if total_findings <= 5: 
        return "HEALTHY"
    elif total_findings <= 15:
        return "WANING"
    else: 
        return "CRITICAL"

def detect_findings_anomaly(
        previous_findings,
        current_findings
):
    if previous_findings == 0: 
        return False
    
    increase_ratio = (
        current_findings / previous_findings
    )
    if increase_ratio > 2.0:
        print(
            "\n[WARNING] Findings Anomaly Detected!"
        )
        print(
            f" Findings increased from "
            f"{previous_findings} "
            f"to {current_findings}"
        )

        return True
    return False

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
