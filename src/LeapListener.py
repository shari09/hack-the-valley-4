import sys
sys.path.insert(0, "./lib/x86")
import Leap


def isDrawPos(hand):
    for finger in hand.fingers:
        if finger.type != Leap.Finger.TYPE_INDEX:
            if finger.is_extended:
                return False
        else:
            if not finger.is_extended:
                return False
    return True


class LeapListener(Leap.Listener):
    def on_connect(self, controller):
        print "lmao"

    def on_frame(self, controller):
        frame = controller.frame()
        if (not frame.hands.is_empty
           and isDrawPos(frame.hands.rightmost)):
            print 'can draw now'
            index = frame.hands.rightmost.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
        else:
            print 'cannot draw'
            # print "Extended:", index.is_extended, "Distance:", index.touch_distance, \
            #     "Zone:", index.touch_zone, "Position:", index.tip_position
            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            #   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        while (hand.fingers.finger_type(Finger.TYPE_INDEX) && hand.fingers.finger_type(Finger.TYPE_THUMB)):
            if hand.PinchStrength <= 1 and hand.PinchStrength > 0.5:
                print "zoom out"
            elif hand.PinchStrength < 0.5  and hand.PinchStrength >= 0:
                print "zoom in"
        
        