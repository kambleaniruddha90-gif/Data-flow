import cv2
import threading


class CameraStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.running = False
        self.frame = None

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                cv2.imshow("Interview Camera", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()