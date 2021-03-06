import sys
import pygame
import pygame.gfxdraw
from Point import Point
sys.path.insert(0, "./lib/x86")
import Leap
from Settings import Settings


def isDrawPos(rightHand):
    for finger in rightHand.fingers:
        if finger.type == Leap.Finger.TYPE_INDEX:
            if not finger.is_extended:
                return False
        else:
            if finger.is_extended:
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

def isSettingPos(hand):
    for finger in hand.fingers:
        if finger.type == Leap.Finger.TYPE_THUMB:
            if finger.is_extended:
                return False
        else:
            if not finger.is_extended:
                return False
    return True


class LeapListener(Leap.Listener):
    def __init__(self, canvas):
        Leap.Listener.__init__(self)
        self.canvas = canvas
        self.finger_pos = Point()
        self.is_drawing = False
        self.lastFrame = None
        self.settingPage = Settings()
        self.settingLock = False
        self.brushSize = 5
        self.eraser = False

    def on_connect(self, controller):
        print 'connected'
        self.lastFrame = controller.frame()

    def on_frame(self, controller):
        frame = controller.frame()
        self.is_drawing = False
        if not frame.hands.is_empty:
            rightHand = frame.hands.rightmost

            # settings page
            if self.settingLock:
                for gesture in frame.gestures():
                    if gesture.type is Leap.Gesture.TYPE_SWIPE:
                        swipe = Leap.SwipeGesture(gesture)
                        print swipe.direction
                        self.settingLock = False
                        # self.settingPage.clear()
                    elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
                        screenTap = Leap.ScreenTapGesture(gesture)
                        tapPoint = screenTap.position
                        # print tapPoint
                        # do something with the tapPoint offset
                        # x = tapPoint.x
                        # y = tapPoint.y
                        index = rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
                        x = int(2*index.stabilized_tip_position[0]+400)
                        y = int(-2*index.stabilized_tip_position[1]+800)
                        clickedButton = self.settingPage.getClicked(x, y)
                        print x, y
                        self.settingLock = False
                        if clickedButton == 'brush size -':
                            self.brushSize -= 1
                        elif clickedButton == 'brush size +':
                            self.brushSize += 1
                        elif clickedButton == 'eraser':
                            self.eraser = True
                        elif clickedButton == 'brush':
                            self.eraser = False
                        else:
                            self.settingLock = True

            # drawing pos
            if isDrawPos(rightHand):
                # print 'can draw now'
                index = rightHand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
                x = int(2*index.stabilized_tip_position[0]+400)
                y = int(-2*index.stabilized_tip_position[1]+800)
                self.finger_pos.x = x
                self.finger_pos.y = y
                if index.touch_distance < 0 and not self.settingLock:
                    self.is_drawing = True
                    colour = (255, 0, 0)
                    if self.eraser:
                        colour = (255, 255, 255)
                    self.canvas.paint(x, y, colour, self.brushSize)
                    # pygame.gfxdraw.aacircle(self.canvas, x, y, 3, (255, 0, 0))
                    # pygame.draw.circle(self.canvas, (255, 0, 0), (x, y), 3)
                    # print index.tip_position[0], index.tip_position[1]
            
            # zooming
            elif isZoomPos(rightHand):
                pinchDiff = (rightHand.pinch_strength
                             - self.lastFrame.hands.rightmost.pinch_strength)
                diffMark = 0
                if pinchDiff > diffMark:
                    print 'zoom out'
                    self.canvas.change_zoom(0.005)
                elif pinchDiff < -diffMark:
                    print 'zoom in'
                    self.canvas.change_zoom(-0.005)

            # settings page
            # elif rightHand.grab_strength == 1:
            elif isSettingPos(rightHand):
                print 'settings page'
                self.settingPage.display()
                self.settingLock = True

                # self.paintSurface.set_alpha(0)
                
            # elif rightHand.grab_strength > 0.5:
            #     # 0.35 radians is approxiamately 20 degrees
            #     rotateMark = 0.02
            #     rotateAngle = rightHand.rotation_angle(
            #                     self.lastFrame, 
            #                     Leap.Vector.y_axis)
            #     if (rightHand.rotation_probability > 0.8):
            #         if (rotateAngle > rotateMark):
            #             print 'clockwise rotation'
            #         elif (rotateAngle < -rotateMark):
            #             print 'counter clockwise'
            #         return
                
            #     print 'move page'
                # for gesture in frame.gestures():
                #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                #         circle = Leap.CircleGesture(gesture)
                #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                #             clockwise = "clockwise"
                #         else:
                #             counterclockwise = "counter-clockwise"
                #         swept_angle = 0
                #         if circle.state != Leap.Gesture.STATE_START:
                #             previous = Leap.CircleGesture(controller.frame(1).gesture(circle.id))
                #             swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                #         print "id: " + str(circle.id) + "progress: " + str(circle.progress) + " Radius: " + str(circle.radius) + " swept angle: " + str(swept_angle * Leap.RAD_TO_DEG) + " " + clockdirection
        else:
            print 'cannot draw'
            # print "Extended:", index.is_extended, "Distance:", index.touch_distance, \
            #     "Zone:", index.touch_zone, "Position:", index.tip_position
            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            #   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        self.lastFrame = frame



        
        
        
