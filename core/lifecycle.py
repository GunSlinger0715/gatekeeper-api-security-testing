# =========================================================
# EXECUTION LIFECYCLE ORCHESTRATION ENGINE
#
# Purpose:
# Centralize orchestration lifecycle awareness across
# GateKeeper security analysis workflows.
#
# Responsibilities:
# - Track active execution phases
# - Maintain deterministic execution ordering
# - Preserve orchestration visibility
# - Support telemetry-aware execution flow
# - Establish phase-oriented subsystem boundaries
#
# Architectural Goal:
# Transition GateKeeper from isolated subsystem execution
# into a lifecycle-aware operational intelligence platform.
#
# Engineering Philosophy:
# From Validation to Operational Intelligence.
# =========================================================

class ExecutionLifecycle:

    def __init__(self):

        self.current_phase = "INITIALIZATION"

        self.completed_phases = []


    def enter_phase(self, phase_name):

        print(f"\n[PHASE] Entering: {phase_name}")

        self.current_phase = phase_name

        self.completed_phases.append(phase_name)


    def get_current_phase(self):

        return self.current_phase


    def print_completed_phases(self):

        print("\n[LIFECYCLE COMPLETE]")

        for phase in self.completed_phases:

            print(f" - {phase}")