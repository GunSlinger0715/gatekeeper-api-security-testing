class Observation: 
    def __init__(self):
        self.type = None

        self.details = None

        self.timestamp = None

        self.evidence = []

        self.confidence = 0

        self.source = None 
    
    def to_dict(self):

        return {

            "type": self.type,

            "details": self.details,

            "timestamp": self.timestamp,

            "evidence": self.evidence,

            "confidence": self.confidence,

            "source": self.source
        }