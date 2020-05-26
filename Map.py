from Graph import Graph
from functions import *
import pygame
import copy
from Player import Player
from Country import Country
import random

class Map(Graph):
  
  #initilize Map instance
  def __init__(self):
   super().__init__()
   self.player_list = []

  def makeNeighbours(self, country1, country2):
    self.add_edge(country1,country2)
    country1.addNeighbour(country2)
    country2.addNeighbour(country1) 
  
  def addPlayer(self, player):
    self.player_list.append(player)

  def playTrainingGame(self):
    data = []
    rewards = []
    edge_index = 0
    permanent_player_list = [p for p in self.player_list]

    player = 0
    fortify = False
    draft = True
    turn = 0

    while len(self.player_list) > 1:
      if draft:
        current_player = self.player_list[player]

      if fortify:
        current_player.fortify()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        current_player.place_reward_random()
        if turn > 8: 
          reward = [-10.0 for i in range(14)]
          reward[edge_index] = current_player.update_num_soldiers()/10
          rewards.append(reward)
          #print('reward')
        else:
          current_player.update_num_soldiers()

        draft = False
      else:
        permanent_player_list.remove(current_player)
        data.append(map_to_array(self,current_player,permanent_player_list[0],permanent_player_list[1]))
        #print('map')
        permanent_player_list.append(current_player)
        attack = current_player.random_attack()

        for i in range(len(self.edges())):
          if attack == self.edges()[i]:
            edge_index = i

        fortify = True
      
      turn += 1

    return (data,rewards)

  def playTrainingGame2(self):
    player1_moves = []
    player2_moves = []
    player3_moves = []
    player1_maps = []
    player2_maps = []
    player3_maps = []
    
    edge_index = 0
    permanent_player_list = [p for p in self.player_list]

    player = 0
    fortify = False
    draft = True
    turn = 0

    while len(self.player_list) > 1:
      if draft:
        current_player = self.player_list[player]

      if fortify:
        current_player.fortify()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        current_player.place_reward_random()
        else:
          current_player.update_num_soldiers()

        draft = False
      else:
        permanent_player_list.remove(current_player)
        data.append(map_to_array(self,current_player,permanent_player_list[0],permanent_player_list[1]))
        #print('map')
        permanent_player_list.append(current_player)
        attack = current_player.random_attack()

        for i in range(len(self.edges())):
          if attack == self.edges()[i]:
            edge_index = i

        fortify = True
      
      turn += 1

    return (data,rewards)


  def playAiGame(self,network,ai_player,display):
    permanent_player_list = [p for p in self.player_list]   
    if display:
      pygame.init()

    run = True

    player = 0
    fortify = False
    draft = True
    while len(self.player_list) > 1 and run:
      if draft:
        current_player = self.player_list[player]
      if display:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        win = pygame.display.set_mode((700,700))
        pygame.display.set_caption('Risk')
        pygame.time.delay(1000)

      if fortify:
        current_player.fortify()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        current_player.place_reward_random()
        draft = False
      else:
        if current_player == ai_player:
          permanent_player_list.remove(ai_player)
          #print('map')
          pred = network.predict([map_to_array(self,ai_player,permanent_player_list[0],permanent_player_list[1])])
          permanent_player_list.append(ai_player)
        
          list_to_attack(list(pred[0]),self,ai_player)
        else:
          current_player.random_attack()

        fortify = True


      if display:    
        self.drawMap(win)
        pygame.display.update()
      
    if display:
      while run:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        if display:
          win = pygame.display.set_mode((700,700))
          pygame.display.set_caption('Risk')
          pygame.time.delay(2500)
        
        if player < len(self.player_list) - 1:
          player += 1
        else:
          player = 0
        if display:    
          self.drawMap(win)
          pygame.display.update()
    print(self.player_list[0].getName())
    print(len(self.player_list))  
    if display:
      pygame.quit()




  def playRandomGame(self, display):

    if display:
      pygame.init()

    run = True

    player = 0
    fortify = False
    draft = True
    while len(self.player_list) > 1 and run:
      if draft:
        current_player = self.player_list[player]
      if display:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        win = pygame.display.set_mode((700,700))
        pygame.display.set_caption('Risk')
        pygame.time.delay(1500)

      if fortify:
        current_player.fortify()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        current_player.place_reward_random()
        draft = False
      else:
        current_player.random_attack()
        fortify = True


      if display:    
        self.drawMap(win)
        pygame.display.update()
      
    if display:
      while run:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        if display:
          win = pygame.display.set_mode((700,700))
          pygame.display.set_caption('Risk')
          pygame.time.delay(2500)
        
        if player < len(self.player_list) - 1:
          player += 1
        else:
          player = 0
        if display:    
          self.drawMap(win)
          pygame.display.update()
    
    if display:
      pygame.quit()



  def removePlayer(self, player):
    self.player_list.remove(player)

  def addCountry(self, country):
    self.add_node(country)
  #edits the print function

  def getPlayerList(self): return self.player_list

  def drawMap(self,window):
   w, h = 700,700
   for edge in self.edges():
     draw_connection(grid_to_coordinates(edge[0].getX(), edge[0].getY(), w, h),grid_to_coordinates(edge[1].getX(), edge[1].getY(), w, h),window)
   for node in self.nodes():
    if not node.getRuler():
      player_colour = (255,255,255)
      print(1)
    elif node.getRuler().getIndex() == 0:
      player_colour = (0,255,0)
    elif node.getRuler().getIndex() == 1:
      player_colour = (255,0,255)
    elif node.getRuler().getIndex() == 2:
      player_colour = (0,255,255)
    else:
      player_colour = (255,255,255)
      print(2)

    if node.getContinent()[0] == 0:
      colour = (0,0,255)
    elif node.getContinent()[0] == 1:
      colour = (255,0,0)
    elif node.getContinent()[0] == 2:
      colour = (0,255,0)
    else:
      colour = (255,255,255)
    position_list = list(grid_to_coordinates(node.getX(),node.getY(),700,700))
    position_tuple = (position_list[0]-5,position_list[1]-10) 

    pygame.draw.circle(window, colour, grid_to_coordinates(node.getX(),node.getY(),700,700), 25)
    pygame.draw.circle(window, player_colour, grid_to_coordinates(node.getX(),node.getY(),700,700), 22)

    font = pygame.font.SysFont(None,30)
    window.blit(font.render(str(node.getSoldiers()), True, (0,0,0)), position_tuple)




  """
  def __str__(self):
    territory_string = ''
    for t in self.territories:
      territory_string += str(t) + ' '
    return str(self.name) + ' ' + territory_string
  """


def build_simple_map():

  my_map = Map()
  Player1 = Player('ai_player', my_map)
  Player2 = Player('player2', my_map)
  Player3 = Player('player3', my_map)
  Player1.resetPlayerIndex()
  Player_list = my_map.getPlayerList()
  ireland = Country('ireland', my_map,5,5,(1,2,3))
  scotland = Country('scotland',my_map,7,5,(0,2,3))
  wales = Country('wales',my_map,7,6,(2,2,3))
  france = Country('france',my_map,6,7,(2,2,3))
  england = Country('england', my_map,6,6,(0,2,3))
  ni = Country('NI', my_map,5,6,(1,2,3))
  my_map.makeNeighbours(england,ireland)
  my_map.makeNeighbours(ni,ireland)
  my_map.makeNeighbours(scotland,wales)
  my_map.makeNeighbours(england,wales)
  my_map.makeNeighbours(england,scotland)
  my_map.makeNeighbours(ireland,scotland)
  my_map.makeNeighbours(wales,france)
  #ireland.setRuler(Player1)
  Player1.addCountry(ireland)
  Player1.addCountry(ni)
  Player2.addCountry(england)
  Player3.addCountry(scotland)
  Player3.addCountry(wales)
  Player2.addCountry(france)
  for node in my_map.nodes():
    node.setSoldiers(random.randint(1,6))

  return my_map