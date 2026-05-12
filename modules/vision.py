class VisionEngine:

    def analyze(self, frame):

        if frame is None:
            return {
                "status": "skipped",
                "detections": [],
                "risk_score": 0.0
            }

        # simulated detection
        return {
            "status": "success",
            "detections": [
                {"object": "person", "confidence": 0.95}
            ],
            "risk_score": 0.1
        }