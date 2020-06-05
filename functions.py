import pygame
import numpy as np
import random
import copy
import Player
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

def six_player_map_to_array(my_map, ai_player, player_list):
  out = []
  for country in my_map.nodes():
    if country.getRuler() == ai_player:
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      
    elif country.getRuler() == player_list[0]:
      out.append(0.0)
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
    
    elif country.getRuler() == player_list[1]:
      out.append(0.0)
      out.append(0.0)
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
    
    elif country.getRuler() == player_list[2]:
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)

    elif country.getRuler() == player_list[3]:
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
      out.append(1.0)
      out.append(0.0)

    else:
      out.append(0.0)
      out.append(0.0)
      out.append(0.0)
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
    """
    if edges[argmax][0].getRuler() == player and edges[argmax][1].getRuler() != player:
      attack = player.attack(edges[argmax][0],edges[argmax][1])
      return attack
      no_move = False
    else:
      my_list[argmax] = -100.0
    """
    attack = player.attack(edges[argmax][0],edges[argmax][1])
    return attack
    no_move = False

    if counter == len(my_list):
      break
    else:
      counter +=1

def list_to_fortify(my_list,my_map,player,fortify_options):
  no_move = True
  counter = 0
  while no_move:
    argmax = 0
    fortify_options
    for i in range(len(my_list)):
      if my_list[argmax] < my_list[i]:
        argmax = i
    if player.is_connected(fortify_options[argmax][0],fortify_options[argmax][1]):
      fortify_move = player.fortify_(fortify_options[argmax][0],fortify_options[argmax][1])
    else:
      fortify_move = None

    if fortify_move:
      return fortify_move
      no_move = False
    else:
      my_list[argmax] = -100.0

    if counter == len(my_list):
      break
    else:
      counter +=1

def list_to_draft(my_list,my_map,player,num_soldiers):
  no_move = True
  counter = 0
  while no_move:
    argmax = 0
    nodes = my_map.nodes()
    for i in range(len(my_list)):
      if my_list[argmax] < my_list[i]:
        argmax = i
        
    if nodes[argmax].getRuler() == player:
      nodes[argmax].setSoldiers(nodes[argmax].getSoldiers() + num_soldiers)
      return nodes[argmax]
    else:
      my_list[argmax] = -100.0

    if counter == len(my_list):
      break
    else:
      counter +=1

def indexs_to_lists(list_of_indexs, length):
    list_of_lists = []
    for i in list_of_indexs:
        new_list = []
        for j in range(length):
            if i == j:
                new_list.append(1.0)
            else:
                new_list.append(0.0)
        list_of_lists.append(new_list)
    return list_of_lists

#Helper function for playTrainingGame()
def training_game_attack(player, player_list,network,map_list,move_list,attack_list,random_pc,my_map):

    player_list.remove(player)
    loop = True
    map_list.append(six_player_map_to_array(my_map,player,player_list))
    if random.randint(0,100) < random_pc:
      attack = player.random_attack()
    else:
      pred = network.predict([six_player_map_to_array(my_map,player, player_list)],batch_size=1)
      attack = list_to_attack(list(pred[0]),my_map,player)

    if not attack:
      del map_list[-1]
    else:
      move_list.append(attack_list.index(attack))
      

    player_list.append(player)

#Helper function for playTrainingGame()

def training_game_fortify(player, player_list,network,map_list,move_list,attack_list,random_pc,my_map):
  
  player_list.remove(player)
  
  map_list.append(six_player_map_to_array(my_map,player,player_list))
  if random.randint(0,100) < random_pc:
    fortify_move = player.fortify_random()
  else:
    pred = network.predict([six_player_map_to_array(my_map,player,player_list)],batch_size=1)
    fortify_move = list_to_fortify(list(pred[0]),my_map,player,attack_list)
                  
  if not fortify_move:
    del map_list[-1]
  else:
    move_list.append(attack_list.index(fortify_move))
  
  player_list.append(player)

def training_game_draft(player, player_list,network,map_list,move_list,random_pc,country_list,my_map):
  player_list.remove(player)
  map_list.append(six_player_map_to_array(my_map,player,player_list))
  

  if random.randint(0,100) < random_pc:
    draft_move = player.place_reward_random()
  else:
    pred = network.predict([six_player_map_to_array(my_map,player,player_list)],batch_size=1)
    draft_move = list_to_draft(list(pred[0]),my_map,player,player.calc_reward())
            
  move_list.append(country_list.index(draft_move))
  player_list.append(player)