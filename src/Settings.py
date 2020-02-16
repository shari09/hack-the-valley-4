import pygame
from Button import Button

class Settings():
  def __init__(self):
    self.surface = pygame.Surface((800, 800), flags=pygame.SRCALPHA)
    # self.surface.set_alpha(255)
    self.buttons = [
      Button(0, 0, 100, 100, 'brush size -', self.surface),
      Button(0, 120, 100, 100, 'brush size +', self.surface),
      Button(120, 0, 100, 100, 'eraser', self.surface)
    ]
  
  def display(self):
    for button in self.buttons:
      button.display()

  def getClicked(self, x, y):
    for button in self.buttons:
      if button.isClicked(x, y):
        return button.text
    return None
  
  # def clear(self):
  #   self.surface.fill((255, 255, 255, 0))
    # self.surface.set_alpha(0)
