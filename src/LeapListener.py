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
        print 'connected'

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty: 
            rightHand = frame.hands.rightmost
            if isDrawPos(rightHand):
                print 'can draw now'
                index = rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
            elif rightHand.grab_strength == 1:
                print 'settings page'
            elif rightHand.grab_strength > 0.5:
                # 0.35 radians is approxiamately 20 degrees
                if rightHand.rotation_angle(self.lastFrame, Leap.Vector.y_axis) > 0.25:
                    print 'clockwise rotation'
                else:
                    print 'move page'
        else:
            print 'cannot draw'
            # print "Extended:", index.is_extended, "Distance:", index.touch_distance, \
            #     "Zone:", index.touch_zone, "Position:", index.tip_position
            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            #   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        
        self.lastFrame = frame
        
        while (hand.fingers.finger_type(Finger.TYPE_INDEX) and hand.fingers.finger_type(Finger.TYPE_THUMB)):
            if  0.5 < hand.PinchStrength <= 1:
                print "zoom out"
            elif 0 >= hand.PinchStrength <= 0.5:
                print "zoom in"
        
        
        
