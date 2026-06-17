from core.observations import Observation
from core.intelligence_record import IntelligenceRecord


obs = Observation()

obs.type = "ENDPOINT_REACHABLE"

obs.details = "GET /json returned 200"

obs.confidence = 100

obs.source = "ENDPOINT_SCANNER"


record = IntelligenceRecord()

record.add_observation(obs)

print(record.observations)