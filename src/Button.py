import pygame

pygame.init()

class Button():
  arial = pygame.font.SysFont('Arial', 30)
  def __init__(self, x, y, width, height, text, surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.text = text
    self.surface = surface
    self.textGraphics = Button.arial.render(self.text, 1, (0, 0, 0))
    self.textRect = self.textGraphics.get_rect(
      center=(self.x+self.width/2, self.y+self.height/2)
    )

  def display(self):
    pygame.draw.rect(self.surface, (220, 220, 220), 
                     (self.x, self.y, self.width, self.height))
    self.surface.blit(self.textGraphics, self.textRect)

  def isClicked(self, x, y):
    return (self.x < x < self.x+self.width 
            and self.y < y < self.y+self.height)