import sys
import pygame
import pygame.gfxdraw
from LeapListener import LeapListener
sys.path.insert(0, "./lib/x86")
import Leap

def draw_cursor(surface, origin, is_drawing):
    pygame.draw.line(surface, (0, 0, 0), (origin[0]-5, origin[1]), (origin[0]+5, origin[1]))
    pygame.draw.line(surface, (0, 0, 0), (origin[0], origin[1]-5), (origin[0], origin[1]+5))
    if is_drawing:
        pygame.gfxdraw.aacircle(surface, origin[0], origin[1], 4, (0, 0, 0))


def main():
    pygame.init()

    display = pygame.display.set_mode((800, 800))
    paint_surface = pygame.Surface((800, 800), flags=pygame.SRCALPHA)

    listener = LeapListener(paint_surface)
    # listener = LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    controller.config.set('Gesture.Swipe.MinLength', 50.0)
    controller.config.set('Gesture.Swipe.MinVelocity', 100)
    controller.config.set('Gesture.ScreenTap.MinForwardVelocity', 20)
    controller.config.set('Gesture.ScreenTap.HistorySeconds', 0.5)
    controller.config.set('Gesture.ScreenTap.MinDistance', 1.0)
    
    controller.config.save()

    running = True
    clock = pygame.time.Clock()
    curSurface = paint_surface

    paint_surface.fill((255, 255, 255))
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
            if listener.settingLock:
                curSurface = listener.settingPage.surface
            else:
                curSurface = paint_surface
            display.blit(curSurface, (0, 0))
            draw_cursor(display, listener.finger_pos, listener.drawing)
            pygame.display.flip()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        pygame.quit()


if __name__ == "__main__":
    main()
