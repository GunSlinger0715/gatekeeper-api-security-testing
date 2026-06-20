from core.observations import Observation
from core.intelligence_record import IntelligenceRecord
from core.observation_factory import create_observation


obs = create_observation(
    observation_type="ENDPOINT_REACHABLE",
    details="GET /json returned 200",
    confidence=100,
    source="ENDPOINT_SCANNER"
)


record = IntelligenceRecord()

record.add_observation(obs)

print(record.observations)