import sys
sys.path.insert(0, "./lib/x86")
import Leap


def isDrawPos(rightHand):
    for finger in rightHand.fingers:
        if finger.type != Leap.Finger.TYPE_INDEX:
            if finger.is_extended:
                return False
        else:
            if not finger.is_extended:
                return False
    return True

def isZoomPos(hand):
    for finger in hand.fingers:
        if (finger.type == Leap.Finger.TYPE_INDEX
            or finger.type == Leap.Finger.TYPE_THUMB):
            if not finger.is_extended:
                return False
        else:
            if finger.is_extended:
                return False
    return True


class LeapListener(Leap.Listener):

    def on_connect(self, controller):
        print 'connected'
        self.lastFrame = controller.frame

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty: 
            rightHand = frame.hands.rightmost
            # drawing pos
            if isDrawPos(rightHand):
                print 'can draw now'
                index = rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
            # full fist
            elif isZoomPos(rightHand):
                pinchDiff = (rightHand.pinch_strength 
                             - self.lastFrame.hands.rightmost.pinch_strength)
                diffMark = 0.05
                if pinchDiff > diffMark:
                    print 'zoom out'
                elif pinchDiff < -diffMark:
                    print 'zoom in'
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
        

        
        # while (rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX) and rightHand.fingers.finger_type(Finger.TYPE_THUMB)):
        #     if  0.5 < rightHand.PinchStrength <= 1:
        #         print "zoom out"
        #     elif 0 >= rightHand.PinchStrength <= 0.5:
        #         print "zoom in"

        # for gesture in frame.guesture():
        #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
        #         circle = CircleGesture(gesture)
        #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
        #             clockwise = "clockwise"
        #         else:
        #             counterclockwise = "counter-clockwise"
        #         swept_angle = 0
        #         if circle.state != Leap.Gesture.STATE_START:
        #             previous = CircleGesture(controller.fram(1).gesture(circle.id))
        #             swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
        #         print "id: " + str(circle.id) + "progress: " + str(circle.progress) + " Radius: " + str(circle.radius) + " swept angle: " + str(swept_angle * Leap.RAD_TO_DEG) + " " + clockdirection
                




        
        
        
