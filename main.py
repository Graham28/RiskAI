import pygame
from functions import *


pygame.init()
run = True
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  win = pygame.display.set_mode((700,700))
  pygame.display.set_caption('Risk')


  
  font = pygame.font.Font(None, 36)
  win.blit(font.render('1', True, black), (495,290))

  pygame.draw.circle(win, red, grid_to_coordinates(8,7,700,700), 25)
  
  pygame.draw.circle(win, blue, grid_to_coordinates(8,7,700,700), 20)

  pygame.draw.circle(win, red, grid_to_coordinates(8,6,700,700), 25)
  
  pygame.draw.circle(win, blue, grid_to_coordinates(8,6,700,700), 20)


    

  
  pygame.display.update()