import sys
import pygame
import pygame.gfxdraw
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
    def __init__(self, surface):
        Leap.Listener.__init__(self)
        self.surface = surface
        self.finger_pos = [0, 0]
        self.drawing = False
        self.lastFrame = None

    def on_connect(self, controller):
        print 'connected'
        self.lastFrame = controller.frame

    def on_frame(self, controller):
        frame = controller.frame()
        self.drawing = False
        if not frame.hands.is_empty:
            rightHand = frame.hands.rightmost
            # drawing pos
            if isDrawPos(rightHand):
                print 'can draw now'
                index = rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
                x = int(2*index.stabilized_tip_position[0]+400)
                y = int(-2*index.stabilized_tip_position[1]+800)
                self.finger_pos[0] = x
                self.finger_pos[1] = y
                if index.touch_distance < 0:
                    self.drawing = True
                    pygame.gfxdraw.aacircle(self.surface, x, y, 5, (255, 0, 0))
                    pygame.draw.circle(self.surface, (255, 0, 0), (x, y), 4)
                    # print index.tip_position[0], index.tip_position[1]
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
                rotateMark = 0.02
                rotateAngle = rightHand.rotation_angle(
                                self.lastFrame, 
                                Leap.Vector.y_axis)
                if (rightHand.rotation_probility) > 0.8:
                    if (rotateAngle > rotateMark):
                        print 'clockwise rotation'
                    elif (rotateAngle < -rotateMark):
                        print 'counter clockwise'
                    return
                
                print 'move page'
        else:
            print 'cannot draw'
            # print "Extended:", index.is_extended, "Distance:", index.touch_distance, \
            #     "Zone:", index.touch_zone, "Position:", index.tip_position
            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            #   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        self.lastFrame = frame
