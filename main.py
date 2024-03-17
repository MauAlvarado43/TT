import threading
from detectors.face_detector import PupileDetector
from ui.menu import Menu

class BlinkAssistant:

    def __init__(self):
        self.blink_callback = None
        self.fixation_callback = None

    def run(self):
        self.listen()
        Menu(self).keep_alive()

    def set_blink_callback(self, callback):
        self.blink_callback = callback

    def set_fixation_callback(self, callback):
        self.fixation_callback = callback

    def listen(self):

        def handle_blink(right_pupile, left_pupile):
            if self.blink_callback is not None:
                self.blink_callback(right_pupile, left_pupile)

        def handle_fixation(right_pupile, left_pupile):
            if self.fixation_callback is not None:
                self.fixation_callback(right_pupile, left_pupile)
        
        def listen_pupile_detector():
            self.pupile_detector = PupileDetector(handle_blink, handle_fixation)
            self.pupile_detector.process_pupile()

        threading.Thread(target=listen_pupile_detector, daemon=True).start()

if __name__ == "__main__":
    BlinkAssistant().run()