import time
import uuid
import json
import os

from io_layer.audio_stream import AudioStream
from io_layer.camera_stream import CameraStream
from io_layer.tts import speak
from pipeline.orchestrator import Pipeline


class InterviewSystem:

    def __init__(self):
        self.pipeline = Pipeline()
        self.session_id = str(uuid.uuid4())

    def start(self):

        question = "Tell me about yourself"
        last_response = None

        # Start streams
        audio = AudioStream()
        camera = CameraStream()

        audio.start()
        camera.start()

        print("🎥 Camera started")
        print("🎤 Listening started")

        speak(question)

        try:
            while True:

                # Check every 2 seconds
                time.sleep(2)

                # Get audio chunk (NUMPY, not file)
                audio_data = audio.get_chunk(5)

                # Skip if silence / no speech
                if audio_data is None:
                    continue

                # Get latest frame
                frame = camera.get_frame()

                # Run pipeline
                result = self.pipeline.run_step(
                    audio_data,
                    frame,
                    question
                )

                # Handle pipeline error
                if "error" in result:
                    print("⚠️ Pipeline error:", result["error"])
                    continue

                score = result["score"]
                decision = result["decision"]

                # Decide next response
                if decision == "repeat":
                    response = "Please elaborate more."
                else:
                    question = self.pipeline.brain.next_question(score)
                    response = question

                # Avoid repeating same response
                if response != last_response:
                    speak(response)
                    last_response = response

                # Stop after 3 Q&A cycles
                if len(self.pipeline.history) >= 3:
                    speak("Interview complete. Thank you.")
                    break

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")

        finally:
            print("🧹 Cleaning up...")

            audio.stop()
            camera.stop()

            self.save()

            print("✅ Session saved")

    def save(self):
        os.makedirs("logs", exist_ok=True)

        data = {
            "session_id": self.session_id,
            "history": self.pipeline.history,
            "report": self.pipeline.generate_report()
        }

        with open(f"logs/{self.session_id}.json", "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    system = InterviewSystem()
    system.start()