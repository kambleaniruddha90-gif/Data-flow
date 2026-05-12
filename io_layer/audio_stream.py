import sounddevice as sd
import numpy as np
import threading
import time


class AudioStream:
    def __init__(self, fs=16000):
        self.fs = fs
        self.buffer = []
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        threading.Thread(target=self._record, daemon=True).start()

    def _record(self):
        def callback(indata, frames, time_info, status):
            if self.running:
                with self.lock:
                    self.buffer.append(indata.copy())

        with sd.InputStream(samplerate=self.fs, channels=1, callback=callback):
            while self.running:
                time.sleep(0.1)

    def get_chunk(self, seconds=5):

        with self.lock:
            if not self.buffer:
                return None

            data = np.concatenate(self.buffer, axis=0)

        samples_needed = int(self.fs * seconds)

        if len(data) < samples_needed:
            return None

        chunk = data[-samples_needed:]

        # silence detection
        if np.abs(chunk).mean() < 0.01:
            return None

        # 🔑 return raw numpy audio
        return chunk

    def stop(self):
        self.running = False