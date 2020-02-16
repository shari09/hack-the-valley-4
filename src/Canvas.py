import pygame
import pygame.gfxdraw
from Point import Point


class Canvas(object):
    def __init__(self, canvas_surface, destination_surface):
        self._canvas = canvas_surface
        self._canvas.fill((255, 255, 255))
        self._zoom = 0.625
        self.origin = Point(canvas_surface.get_width()/2-destination_surface.get_width()/2,
                            canvas_surface.get_height()/2-destination_surface.get_height()/2)
        self.view_subsurf = canvas_surface.subsurface((self.origin.x, self.origin.y),
                                                      destination_surface.get_size())
        self.destination_buffer = pygame.Surface(canvas_surface.get_size())
        self.destination_surface = destination_surface
        self.requires_update = True

    def paint(self, view_x, view_y, colour, size):
        if self._zoom < 1:
            x = int((float(view_x)/self.destination_surface.get_width())*(self._canvas.get_width()*self._zoom)+self.origin.x)
            y = int((float(view_y)/self.destination_surface.get_height())*(self._canvas.get_height()*self._zoom)+self.origin.y)
        else:
            x = int((float(view_x)/self.destination_surface.get_width())*(self.view_subsurf.get_width())+self.origin.x)
            y = (view_y + self.origin.y)
        print "(", view_x, view_y, ")",\
              self.destination_surface.get_size(),\
              self._canvas.get_size(), self._zoom,\
              "(", self.origin.x, self.origin.y, ") (", x, y, ")"
        self.requires_update = True
        pygame.gfxdraw.aacircle(self._canvas, x, y, size, colour)
        pygame.draw.circle(self._canvas, colour, (x, y), size)

    def update(self):
        if self.requires_update:
            # self.view_buffer.blit(self._canvas, (0, 0),
            #                       pygame.Rect(self.origin,
            #                                   self.view_buffer.get_size()))
            if self._zoom < 1:
                pygame.transform.scale(self.view_subsurf, self.destination_surface.get_size(),
                                       self.destination_surface)
            else:
                size = (int(self.destination_surface.get_width()/self._zoom), int(self.destination_surface.get_height()/self._zoom))
                pygame.transform.scale(self.view_subsurf, size,
                                       self.destination_surface.subsurface(pygame.Rect((self.destination_surface.get_width()/2-size[0]/2,
                                                                                        self.destination_surface.get_height()/2-size[1]/2), size)))
            # self.requires_update = False

    def get_view_size(self):
        if self._zoom >= 1:
            return self._canvas.get_size()
        else:
            return (int(self._canvas.get_width()*self._zoom),
                    int(self._canvas.get_height()*self._zoom))

    def change_zoom(self, dzoom):
        old_view_middle = self.origin.translate_new(self.view_subsurf.get_width()/2,
                                                    self.view_subsurf.get_height()/2)
        self._zoom += dzoom
        self.view_subsurf = self._canvas.subsurface(pygame.Rect((self.origin.x, self.origin.y),
                                                                self.get_view_size()))
        # self.view_buffer = pygame.Surface(new_view_size)

        self.origin = old_view_middle.translate_new(-self.view_subsurf.get_width()/2,
                                                    -self.view_subsurf.get_height()/2)
        self.origin.x = max(0, self.origin.x)
        self.origin.y = max(0, self.origin.y)
