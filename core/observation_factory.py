# =========================================================
# OBSERVATION FACTORY
#
# Purpose:
# Centralize creation of Observation objects across
# OVERWATCH subsystems.
#
# Responsibilities:
# - Enforce observation creation standards
# - Apply consistent timestamps
# - Normalize intelligence metadata
# - Ensure uniform observation structure
# - Support future observation enrichment
#
# Architectural Goal:
# Establish a single source of truth for how
# intelligence observations are created and
# represented throughout the OVERWATCH platform.
#
# Benefits:
# - Consistent observation formatting
# - Simplified subsystem integration
# - Easier ingestion into Monolith
# - Improved search, correlation, and analytics
# - Reduced duplication across scanners
#
# Engineering Philosophy:
# Standardized Intelligence Begins Here.
# =========================================================
from datetime import datetime

from core.observations import Observation

def create_observation(
        observation_type,
        details, 
        confidence, 
        source, 
        evidence=None
):
    
    obs = Observation ()

    obs.type = observation_type

    obs.details = details

    obs.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    obs.confidence = confidence

    obs.source = source

    obs.evidence = evidence or []

    return obs
