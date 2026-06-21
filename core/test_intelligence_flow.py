print("TEST FILE VERSION 2")

from core.intelligence_record import IntelligenceRecord
from core.observation_factory import create_observation
from core.context import ExecutionContext


obs = create_observation(
    observation_type="ENDPOINT_REACHABLE",
    details="GET /json returned 200",
    confidence=100,
    source="ENDPOINT_SCANNER"
)


record = IntelligenceRecord()

record.add_observation(obs)

from core.context import ExecutionContext

context = ExecutionContext("/json")

context.add_observation(obs)

print("=== CONTEXT ===")
print(context.to_dict())

print("=== RECORD ===")
print(record.observations)