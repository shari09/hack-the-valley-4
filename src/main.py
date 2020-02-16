import sys
import pygame
import pygame.gfxdraw
from LeapListener import LeapListener
from Canvas import Canvas
sys.path.insert(0, "./lib/x86")
import Leap


def draw_cursor(surface, origin, is_drawing):
    pygame.draw.line(surface, (0, 0, 0), (origin.x-5, origin.y), (origin.x+5, origin.y))
    pygame.draw.line(surface, (0, 0, 0), (origin.x, origin.y-5), (origin.x, origin.y+5))
    if is_drawing:
        pygame.gfxdraw.aacircle(surface, origin.x, origin.y, 4, (0, 0, 0))


def main():
    pygame.init()

    display = pygame.display.set_mode((800, 800))
    draw_canvas = Canvas(pygame.Surface((1280, 1280), flags=pygame.SRCALPHA), display)
    # paint_surface = pygame.Surface((800, 800))

    listener = LeapListener(draw_canvas)
    # listener = LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    controller.config.set('Gesture.Swipe.MinLength', 50.0)
    controller.config.set('Gesture.Swipe.MinVelocity', 100)
    controller.config.set('Gesture.ScreenTap.MinForwardVelocity', 10)
    controller.config.set('Gesture.ScreenTap.HistorySeconds', 0.5)
    controller.config.set('Gesture.ScreenTap.MinDistance', 0.5)

    controller.config.save()

    running = True
    clock = pygame.time.Clock()
    # curSurface = paint_surface

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        draw_canvas.change_zoom(0.025)
                    elif event.key == pygame.K_s:
                        draw_canvas.change_zoom(-0.025)
            clock.tick(60)
            display.fill((0, 0, 0))
            if listener.settingLock:
                display.blit(listener.settingPage.surface, (0, 0))
                # curSurface = listener.settingPage.surface
            else:
                draw_canvas.update()
                # curSurface = paint_surface
            # display.blit(curSurface, (0, 0))
            # draw_canvas.update()
            draw_cursor(display, listener.finger_pos, listener.is_drawing)
            pygame.display.flip()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        pygame.quit()


if __name__ == "__main__":
    main()
