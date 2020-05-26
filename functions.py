import pygame
import numpy as np
#from Map import Map


def grid_to_coordinates(x,y,win_x,win_y):
  return (int((win_x*x)/10), int(win_y - (win_y*y)/10))

def draw_connection(country1,country2,window):
  pygame.draw.line(window,(255,255,255),country1,country2)


def map_to_array(my_map, ai_player, player2, player3):
  out = []
  for country in my_map.nodes():
    if country.getRuler() == ai_player:
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)
    elif country.getRuler() == player2:
      out.append(0.0)
      out.append(1.0)
      out.append(0.0)
    else:
      out.append(0.0)
      out.append(0.0)
      out.append(1.0)
    
    out.append(country.getSoldiers()/50)

  return out

def list_to_attack(my_list,my_map,player):
  no_move = True
  counter = 0
  while no_move:
    argmax = 0
    edges = my_map.edges()
    for i in range(len(my_list)):
      if my_list[argmax] < my_list[i]:
        argmax = i

    if edges[argmax][0].getRuler() == player:
      player.attack(edges[argmax][0],edges[argmax][1])
      no_move = False
    else:
      my_list[argmax] = -1.0

    if counter == len(my_list):
      break
    else:
      counter +=1

