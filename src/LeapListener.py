import sys
sys.path.insert(0, "./lib/x86")
import Leap


class LeapListener(Leap.Listener):
    def on_connect(self, controller):
        print "lmao"

    def on_frame(self, controller):
        frame = controller.frame()
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
          frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
