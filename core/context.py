# =========================================================
# EXECUTION CONTEXT MANAGEMENT ENGINE
#
# Purpose:
# Centralize shared orchestration execution state across
# GateKeeper security analysis workflows.
#
# Responsibilities:
# - Maintain execution-state awareness
# - Centralize findings aggregation
# - Preserve operational telemetry context
# - Support lifecycle-aware orchestration
# - Provide a unified execution intelligence model
#
# Architectural Goal:
# Transition GateKeeper from isolated subsystem execution
# into a context-aware operational intelligence platform.
#
# Future Expansion:
# - Historical telemetry baselining
# - Heimdall visualization workflows
# - Execution anomaly detection
# - Correlated orchestration analytics
# - Adaptive execution behavior
#
# Engineering Philosophy:
# From Orchestration to Execution Intelligence.
# =========================================================

class ExecutionContext:

    def __init__(self, endpoint):

        self.endpoint = endpoint

        self.findings = []

        self.score = 0

        self.risk = None

        self.current_phase = None

        self.stability = None


    def add_findings(self, findings):

        self.findings.extend(findings)


    def set_score(self, score):

        self.score = score


    def set_risk(self, risk):

        self.risk = risk


    def set_phase(self, phase):

        self.current_phase = phase

    def set_stability(self, stability):

        self.stability = stability
    
    def to_dict(self):

        return {
            "endpoint": self.endpoint,
            "score": self.score,
            "risk": self.risk,
            "current_phase": self.current_phase,
            "stability": self.stability,
            "findings": self.findings
        }