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


def map_to_array(my_map, ai_player, player_list):
  out = []
  temp_player_list = copy.deepcopy(player_list)

  for country in my_map.nodes():
    if country.getRuler() == ai_player:
      out.append(1.0)
      out.append(0.0)
      out.append(0.0)
    elif country.getRuler() == temp_player_list[0]:
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
  if my_map.getLastAttacker() == ai_player:
    out.append(1.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
    
  elif my_map.getLastAttacker() == player_list[0]:
    out.append(0.0)
    out.append(1.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
  
  elif my_map.getLastAttacker() == player_list[1]:
    out.append(0.0)
    out.append(0.0)
    out.append(1.0)
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
  
  elif my_map.getLastAttacker() == player_list[2]:
    out.append(0.0)
    out.append(0.0)
    out.append(0.0)
    out.append(1.0)
    out.append(0.0)
    out.append(0.0)

  elif my_map.getLastAttacker() == player_list[3]:
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


    if argmax == len(my_list) - 1:
      return None

    elif edges[argmax] == -100.0:
      attack = None
      no_move = False
    
    elif edges[argmax][0].getRuler() == player and edges[argmax][1].getRuler() != player and edges[argmax][0].getSoldiers() != 1:
      
      attack = player.attack(edges[argmax][0],edges[argmax][1])
      return attack
      no_move = False

    else:
      my_list[argmax] = -100.0
    """
    if argmax == len(edges):
      attack = None
    else:
      attack = player.attack(edges[argmax][0],edges[argmax][1])
    """
    #if attack[0].getRuler() != player or victim.getRuler() == player:


    if counter == len(my_list):
      return None
      break
    else:
      counter +=1
  return attack

def list_to_fortify(my_list,my_map,player,fortify_options):
  no_move = True
  counter = 0
  while no_move:
    argmax = 0
    fortify_options
    for i in range(len(my_list)):
      if my_list[argmax] < my_list[i]:
        argmax = i
    if argmax == len(my_list) - 1:
      return None
    else:
      if player.is_connected(fortify_options[argmax][0],fortify_options[argmax][1]):
        fortify_move = player.fortify_(fortify_options[argmax][0],fortify_options[argmax][1])
      else:
        fortify_move = None

      if fortify_move:
        return fortify_move
        no_move = False
      else:
        return None #test
        no_move = False #test
        #my_list[argmax] = -100.0

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
              if j == length - 1:
                new_list.append(0.006)
              else:
                new_list.append(1.0)
            else:
                new_list.append(0.0)
        list_of_lists.append(new_list)
    return list_of_lists

#Helper function for playTrainingGame()
def training_game_attack(player, player_list,network,map_list,move_list,attack_list,random_pc,my_map,self_play=False):

    player_list.remove(player)
    loop = True

    attack_count = 0
    while True:
      if len(player_list) == 2:
        map_list.append(map_to_array(my_map,player,player_list))
      else:
        map_list.append(six_player_map_to_array(my_map,player,player_list))

      random_num = random.randint(0,99) 

      if random_num < random_pc:
        attack_was_random = True
        attack = player.random_attack()
      else:
        attack_was_random = False
        if len(player_list) == 2:
          pred = network.predict([map_to_array(my_map,player, player_list)],batch_size=1)
        else:
          pred = network.predict([six_player_map_to_array(my_map,player, player_list)],batch_size=1)
          #print(pred)
        attack = list_to_attack(list(pred[0]),my_map,player)

      #if attack == None or attack_count == 10:
      if attack_count == 3:
        if self_play and not attack_was_random:
          move_list.append(pred[0].tolist())
        else:
          if attack != None:
            move_list.append(attack_list.index(attack))
          else:
            move_list.append(len(attack_list))
            #del map_list[-1]
        break

      elif attack == None:
        if self_play and not attack_was_random:
          move_list.append(pred[0].tolist())
        else:
          move_list.append(len(attack_list))
          #del map_list[-1]
        attack_count += 1

      else:
        if self_play and not attack_was_random:
          move_list.append(pred[0].tolist())
        else:
          move_list.append(attack_list.index(attack))
        attack_count += 1

    
      

    player_list.append(player)

#Helper function for playTrainingGame()

def training_game_fortify(player, player_list,network,map_list,move_list,attack_list,random_pc,my_map):
  
  player_list.remove(player)
  if len(player_list) == 2:
    map_list.append(map_to_array(my_map,player,player_list))
  else:
    map_list.append(six_player_map_to_array(my_map,player,player_list))
        
  #if random.randint(0,100) < random_pc:
  if True:
    fortify_move = player.fortify_random()
  else:
    if len(player_list) == 2:
      pred = network.predict([map_to_array(my_map,player, player_list)],batch_size=1)
    else:
      pred = network.predict([six_player_map_to_array(my_map,player, player_list)],batch_size=1)

    fortify_move = list_to_fortify(list(pred[0]),my_map,player,attack_list)
                  
  if not fortify_move:
    #del map_list[-1]
    move_list.append(len(attack_list))
  else:
    move_list.append(attack_list.index(fortify_move))
  
  player_list.append(player)

def training_game_draft(player, player_list,network,map_list,move_list,random_pc,country_list,my_map):
  player_list.remove(player)
  
  if len(player_list) == 2:
    map_list.append(map_to_array(my_map,player,player_list))
  else:
    map_list.append(six_player_map_to_array(my_map,player,player_list))
        
  

  #if random.randint(0,100) < random_pc:
  if True:
    draft_move = player.place_reward_random()
  else:
    if len(player_list) == 2:
      pred = network.predict([map_to_array(my_map,player, player_list)],batch_size=1)
    else:
      pred = network.predict([six_player_map_to_array(my_map,player, player_list)],batch_size=1)

    draft_move = list_to_draft(list(pred[0]),my_map,player,player.calc_reward())
            
  move_list.append(country_list.index(draft_move))
  player_list.append(player)