from modules.stt_engine import STTEngine
from modules.vision import VisionEngine
from modules.brain import Brain


class Pipeline:

    def __init__(self):
        self.stt = STTEngine()
        self.vision = VisionEngine()
        self.brain = Brain()
        self.history = []

    def safe_stt(self, audio):

        for _ in range(3):
            result = self.stt.transcribe(audio)
            if result["status"] == "success":
                return result

        return {
            "status": "failed",
            "text": "No answer",
            "confidence": 0.0
        }

    def run_step(self, audio, frame, question):

        stt = self.safe_stt(audio)

        text = stt["text"][:500]

        vision = self.vision.analyze(frame)

        llm = self.brain.evaluate(text)

        decision = self.brain.decide(
            llm["score"],
            vision["risk_score"]
        )

        result = {
            "question": question,
            "answer": text,
            "score": llm["score"],
            "risk_score": vision["risk_score"],
            "decision": decision
        }

        self.history.append(result)

        return result

    def generate_report(self):

        avg = sum(x["score"] for x in self.history) / len(self.history)

        return {
            "total_questions": len(self.history),
            "average_score": avg,
            "final_decision": "pass" if avg >= 6 else "fail"
        }