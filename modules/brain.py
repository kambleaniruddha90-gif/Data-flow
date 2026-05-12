class Brain:

    def evaluate(self, text):

        if not text:
            return {
                "status": "failed",
                "score": 0,
                "feedback": "No answer"
            }

        score = min(10, len(text.split()) // 5 + 3)

        return {
            "status": "success",
            "score": score,
            "feedback": "Evaluated"
        }

    def decide(self, score, risk):

        if risk > 0.7:
            return "flag_for_review"

        if score >= 7:
            return "next_question"

        return "repeat"

    def next_question(self, score):

        if score >= 7:
            return "Explain a system you designed."

        return "Can you elaborate more?"