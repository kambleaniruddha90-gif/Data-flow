import whisper
import numpy as np


class STTEngine:
    def __init__(self):
        print("🔄 Loading Whisper model...")
        self.model = whisper.load_model("base")
        print("✅ Whisper ready")

    def transcribe(self, audio_array):

        if audio_array is None:
            return {
                "status": "failed",
                "text": "",
                "confidence": 0.0,
                "error": "no audio"
            }

        try:
            # 🔑 Convert to float32 (Whisper requirement)
            audio = audio_array.astype(np.float32).flatten()

            result = self.model.transcribe(audio)

            text = result.get("text", "").strip()

            if not text:
                return {
                    "status": "failed",
                    "text": "",
                    "confidence": 0.0,
                    "error": "empty transcription"
                }

            return {
                "status": "success",
                "text": text,
                "confidence": 0.9,
                "error": None
            }

        except Exception as e:
            return {
                "status": "failed",
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }