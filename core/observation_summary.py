# ============================================
# Observation Intelligence
# ============================================

def summarize_observations(observations):
    """
    Summarize observations collected during execution.
    """

    summary = {
        "total": 0,
        "average_confidence": 0,
        "sources": [],
        "types": []
    }
    
    summary["total"] = len(observations)

    if observations: 
        total_confidence = sum(obs["confidence"] for obs in observations)
        summary["average_confidence"] = round(
            total_confidence / len(observations), 2
        )

    summary["sources"] = sorted(
        list({obs["source"] for obs in observations})
    )

    summary["types"] = sorted(
        list({obs["type"] for obs in observations})
    )

    return summary