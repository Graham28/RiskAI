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
   self.last_successful_attacker = None
  
  def setLastAttacker(self,player):
    self.last_successful_attacker = player

  def getLastAttacker(self):
    return self.last_successful_attacker

  def makeNeighbours(self, country1, country2):
    self.add_edge(country1,country2)
    country1.addNeighbour(country2)
    country2.addNeighbour(country1) 
  
  def addPlayer(self, player):
    self.player_list.append(player)


  def playTrainingGame3(self,attack_network,fortify_network,draft_network):
    attacks_moves = [[],[],[],[],[],[]]
    attack_maps = [[],[],[],[],[],[]]

    fortify_moves = [[],[],[],[],[],[]]
    fortify_maps = [[],[],[],[],[],[]]

    draft_moves = [[],[],[],[],[],[]]
    draft_maps = [[],[],[],[],[],[]]


    attack_list = self.edges()
    country_list = self.nodes()
    fortify_list = []

    for n in self.nodes():
      for c in self.nodes():
        if n != c:
          fortify_list.append([c,n])


    permanent_player_list = [p for p in self.player_list]
    temp_player_list = [p for p in self.player_list]

    player = 0
    fortify = False
    draft = True
    turn = 0

    while len(self.player_list) > 1:
      
      if draft:
        current_player = self.player_list[player]
        training_game_draft(current_player, temp_player_list,draft_network,draft_maps[permanent_player_list.index(current_player)],draft_moves[permanent_player_list.index(current_player)],current_player.getRandomness(),country_list,self)
        current_player.update_num_soldiers()
        draft = False

      if fortify:
        training_game_fortify(current_player, temp_player_list,fortify_network,fortify_maps[permanent_player_list.index(current_player)],fortify_moves[permanent_player_list.index(current_player)],fortify_list,current_player.getRandomness(),self)
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0

      else:
        training_game_attack(current_player, temp_player_list,attack_network,attack_maps[permanent_player_list.index(current_player)],attacks_moves[permanent_player_list.index(current_player)],attack_list,current_player.getRandomness(),self)
        fortify = True
      
      turn += 1
      #if turn%1000 == 0:
      #  print(turn)
      if turn > 3000:
        return None
    return (attack_maps[permanent_player_list.index(self.player_list[0])],indexs_to_lists(attacks_moves[permanent_player_list.index(self.player_list[0])],len(attack_list) +1),fortify_maps[permanent_player_list.index(self.player_list[0])],indexs_to_lists(fortify_moves[permanent_player_list.index(self.player_list[0])],len(fortify_list) + 1),draft_maps[permanent_player_list.index(self.player_list[0])],indexs_to_lists(draft_moves[permanent_player_list.index(self.player_list[0])],len(country_list)),self.player_list[0].getRandomness())
    




  def playAiGame(self,network, fortify_network, ai_player,draft_network,display):
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

        if current_player == ai_player:
          permanent_player_list.remove(ai_player)
          #print('map')
          pred = fortify_network.predict([map_to_array(self,ai_player,permanent_player_list[0],permanent_player_list[1])])
          permanent_player_list.append(ai_player)
        
          list_to_fortify(list(pred[0]),self,ai_player)
        else:
          current_player.fortify_random()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        if current_player == ai_player:
          pred = draft_network.predict([map_to_array(self,current_player,permanent_player_list[0],permanent_player_list[1])])
          draft_move = list_to_draft(list(pred[0]),self,current_player,current_player.calc_reward())

        else:
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

  def playAiGame2(self,network, fortify_network, ai_player,draft_network,display):
    permanent_player_list = [p for p in self.player_list]
    temp_player_list = [t for t in self.player_list]   
    fortify_list = []

    for n in self.nodes():
      for c in self.nodes():
        if n != c:
          fortify_list.append([c,n])

    if display:
      pygame.init()

    run = True
    player = 0
    fortify = False
    draft = True
    count = 0
    while len(self.player_list) > 1 and run:
      if draft:
        count += 1
        if count == 1000:
          run = False
        #print(count)  
        current_player = self.player_list[player]
      if display:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        win = pygame.display.set_mode((700,700))
        pygame.display.set_caption('Risk')
        pygame.time.delay(1)

      if fortify:

        if current_player == ai_player:
          permanent_player_list.remove(ai_player)
          #print('map')
          pred = fortify_network.predict([six_player_map_to_array(self,ai_player,permanent_player_list)])
          permanent_player_list.append(ai_player)
        
          list_to_fortify(list(pred[0]),self,ai_player,fortify_list)
        else:
          current_player.fortify_random()
        fortify = False
        draft = True

        if player < len(self.player_list) - 1:
          player += 1

        else:
          player = 0
      elif draft:
        if current_player == ai_player:
          permanent_player_list.remove(ai_player)
          pred = draft_network.predict([six_player_map_to_array(self,current_player,permanent_player_list)])
          permanent_player_list.append(ai_player)
          draft_move = list_to_draft(list(pred[0]),self,current_player,current_player.calc_reward())

        else:
          current_player.place_reward_random()

        draft = False
      else:
        attack_count = 0
        while True:
          if current_player == ai_player:
            permanent_player_list.remove(ai_player)
            #print('map')
            pred = network.predict([six_player_map_to_array(self,ai_player,permanent_player_list)])
            permanent_player_list.append(ai_player)
          
            attack = list_to_attack(list(pred[0]),self,ai_player)
          else:
            attack = current_player.random_attack()

          if attack == None or attack_count == 10:
            break
          
          attack_count += 1

        fortify = True


      if display:    
        self.drawMap(win)
        pygame.display.update()
      
    if display:
      print(count)
      while run:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
        if display:
          win = pygame.display.set_mode((700,700))
          pygame.display.set_caption('Risk')
        
        if player < len(self.player_list) - 1:
          player += 1
        else:
          player = 0
        if display:    
          self.drawMap(win)
          pygame.display.update()
    print(self.player_list[0].getName())
    print(count)
    if display:
      pygame.quit()
    
    if run == False:
      return ''
    return self.player_list[0].getName()




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
        pygame.time.delay(2000)

      if fortify:
        current_player.fortify_random()
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
          pygame.time.delay(500)
        
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
    elif node.getRuler().getIndex() == 0:
      player_colour = (0,255,0)
    elif node.getRuler().getIndex() == 1:
      player_colour = (255,0,255)
    elif node.getRuler().getIndex() == 2:
      player_colour = (0,0,255)
    elif node.getRuler().getIndex() == 3:
      player_colour = (255,0,0)
    elif node.getRuler().getIndex() == 4:
      player_colour = (255,255,0)
    elif node.getRuler().getIndex() == 5:
      player_colour = (0,255,255)
    else:
      player_colour = (255,255,255)

    if node.getContinent()[0] == 0:
      colour = (0,0,255)
    elif node.getContinent()[0] == 1:
      colour = (255,0,0)
    elif node.getContinent()[0] == 2:
      colour = (0,255,0)
    elif node.getContinent()[0] == 3:
      colour = (255,255,0)
    elif node.getContinent()[0] == 4:
      colour = (0,255,255)
    elif node.getContinent()[0] == 5:
      colour = (255,0,255)
    else:
      colour = (255,255,255)
    position_list = list(grid_to_coordinates(node.getX(),node.getY(),700,700))
    position_tuple = (position_list[0]-5,position_list[1]-10) 

    pygame.draw.circle(window, colour, grid_to_coordinates(node.getX(),node.getY(),700,700), 30)
    pygame.draw.circle(window, player_colour, grid_to_coordinates(node.getX(),node.getY(),700,700), 25)

    font = pygame.font.SysFont(None,30)
    window.blit(font.render(str(node.getSoldiers()), True, (0,0,0)), position_tuple)




  """
  def __str__(self):
    territory_string = ''
    for t in self.territories:
      territory_string += str(t) + ' '
    return str(self.name) + ' ' + territory_string
  """


def build_simple_six_map():

  my_map = Map()
  gradient_of_randomness = [0,15,30,80,90,100]
  random.shuffle(gradient_of_randomness)
  Player1 = Player('ai_player', my_map,gradient_of_randomness[0])
  Player2 = Player('player2', my_map,gradient_of_randomness[1])
  Player3 = Player('player3', my_map,gradient_of_randomness[2])
  Player4 = Player('player4', my_map,gradient_of_randomness[3])
  Player5 = Player('player5', my_map,gradient_of_randomness[4])
  Player6 = Player('player6', my_map,gradient_of_randomness[5])
  Player1.resetPlayerIndex()
  Player_list = my_map.getPlayerList()
  ireland = Country('ireland', my_map,5,5,(1,2,3))
  scotland = Country('scotland',my_map,7,5,(0,2,10))
  wales = Country('wales',my_map,7,6,(2,2,3))
  france = Country('france',my_map,6,7,(2,2,3))
  england = Country('england', my_map,6,6,(0,2,10))
  ni = Country('NI', my_map,5,6,(1,2,3))
  Country_list = my_map.nodes()
  my_map.makeNeighbours(england,ireland)
  my_map.makeNeighbours(ni,ireland)
  my_map.makeNeighbours(scotland,wales)
  my_map.makeNeighbours(england,wales)
  my_map.makeNeighbours(england,scotland)
  my_map.makeNeighbours(ireland,scotland)
  my_map.makeNeighbours(wales,france)
  #ireland.setRuler(Player1)
  index_list = [0,1,2,3,4,5]
  random.shuffle(index_list)
  counter = 0
  while counter < len(Country_list):
    
    if counter%len(index_list) == 0:
      random.shuffle(index_list)
    Player_list[index_list[counter%len(index_list)]].addCountry(Country_list[counter])
    
    counter += 1
    
  #Player1.addCountry(ireland)
  #Player1.addCountry(ni)
  #Player2.addCountry(england)
  #Player3.addCountry(scotland)
  #Player3.addCountry(wales)
  #Player2.addCountry(france)


  #for node in my_map.nodes():
  #  node.setSoldiers(random.randint(1,6))
  for i in range(16):
    for player in Player_list:
      player.place_random_soldier()

  return my_map

def build_full_map():

  my_map = Map()
  gradient_of_randomness = [100,100,100,100,100,100]
  random.shuffle(gradient_of_randomness)
  Player1 = Player('ai_player', my_map,gradient_of_randomness[0])
  Player2 = Player('player2', my_map,gradient_of_randomness[1])
  Player3 = Player('player3', my_map,gradient_of_randomness[2])
  Player4 = Player('player4', my_map,gradient_of_randomness[3])
  Player5 = Player('player5', my_map,gradient_of_randomness[4])
  Player6 = Player('player6', my_map,gradient_of_randomness[5])
  Player1.resetPlayerIndex()
  Player_list = my_map.getPlayerList()

  #Countries
  #North America
  alaska = Country('alaska', my_map,1,9,(0,9,5))
  NWterritory = Country('NWterritory', my_map,2,8,(0,9,5))
  alberta = Country('alberta', my_map,1,7,(0,9,5))
  greenland = Country('greenland', my_map,3,8,(0,9,5))
  ontario = Country('ontario', my_map,2,7,(0,9,5))
  quebec = Country('quebec', my_map,3,7,(0,9,5))
  WUS = Country('WUS', my_map,1,6,(0,9,5))
  EUS = Country('EAS', my_map,2,6,(0,9,5))
  central_america = Country('central_america', my_map,1,5,(0,9,5))
  #NA Neighbours
  my_map.makeNeighbours(alaska,NWterritory)
  my_map.makeNeighbours(alaska,alberta)
  my_map.makeNeighbours(alberta,NWterritory)
  my_map.makeNeighbours(greenland,NWterritory)
  my_map.makeNeighbours(greenland,quebec)
  my_map.makeNeighbours(greenland,ontario)
  my_map.makeNeighbours(alberta,ontario)
  my_map.makeNeighbours(alberta,WUS)
  my_map.makeNeighbours(ontario,WUS)
  my_map.makeNeighbours(ontario,EUS)
  my_map.makeNeighbours(quebec,EUS)
  my_map.makeNeighbours(WUS,EUS)
  my_map.makeNeighbours(WUS,central_america)
  my_map.makeNeighbours(EUS,central_america)

  #South America
  venezuela = Country('venezuela', my_map,1,4,(1,4,2))
  peru = Country('peru', my_map,1,3,(1,4,2))
  brazil = Country('brazil', my_map,2,3,(1,4,2))
  argentina = Country('argentina', my_map,1,2,(1,4,2))

  my_map.makeNeighbours(central_america,venezuela)
  my_map.makeNeighbours(venezuela,peru)
  my_map.makeNeighbours(venezuela,brazil)
  my_map.makeNeighbours(argentina,peru)
  my_map.makeNeighbours(argentina,brazil)

  #Europe
  iceland = Country('iceland', my_map,4,8,(2,7,5))
  scandinavia = Country('scandinavia', my_map,5,8,(2,7,5))
  ukraine = Country('ukraine', my_map,6,7,(2,7,5))
  GB = Country('GB', my_map,4,7,(2,7,5))
  NEU = Country('NEU', my_map,5,7,(2,7,5))
  WEU = Country('WEU', my_map,4,6,(2,7,5))
  SEU = Country('SEU', my_map,5,6,(2,7,5))

  my_map.makeNeighbours(iceland,greenland)
  my_map.makeNeighbours(iceland,scandinavia)
  my_map.makeNeighbours(iceland,GB)
  my_map.makeNeighbours(scandinavia,GB)
  my_map.makeNeighbours(scandinavia,NEU)
  my_map.makeNeighbours(scandinavia,ukraine)
  my_map.makeNeighbours(GB,NEU)
  my_map.makeNeighbours(GB,WEU)
  my_map.makeNeighbours(NEU,ukraine)
  my_map.makeNeighbours(NEU,WEU)
  my_map.makeNeighbours(NEU,SEU)
  my_map.makeNeighbours(ukraine,SEU)

  #Africa
  north_africa = Country('north_africa', my_map,4,4,(3,6,3))
  egypt = Country('egypt', my_map,5,4,(3,6,3))
  east_africa = Country('east_africa', my_map,5,3,(3,6,3))
  congo = Country('congo', my_map,4,3,(3,6,3))
  south_africa = Country('south_africa', my_map,4,2,(3,6,3))
  madagascar = Country('madagascar', my_map,5,2,(3,6,3))

  my_map.makeNeighbours(north_africa,brazil)
  my_map.makeNeighbours(north_africa,SEU)
  my_map.makeNeighbours(north_africa,WEU)
  my_map.makeNeighbours(egypt,SEU)
  my_map.makeNeighbours(north_africa,egypt)
  my_map.makeNeighbours(north_africa,east_africa)
  my_map.makeNeighbours(north_africa,congo)
  my_map.makeNeighbours(egypt,east_africa)
  my_map.makeNeighbours(east_africa,congo)
  my_map.makeNeighbours(east_africa,south_africa)
  my_map.makeNeighbours(east_africa,madagascar)
  my_map.makeNeighbours(congo,south_africa)
  my_map.makeNeighbours(south_africa,madagascar)

  #Asia
  middle_east = Country('middle_east', my_map,6,5,(4,12,7))
  afghanistan = Country('afghanistan', my_map,7,6,(4,12,7))
  ural = Country('ural', my_map,7,7,(4,12,7))
  siberia = Country('siberia', my_map,8,7,(4,12,7))
  yakutsk = Country('yakutsk', my_map,7,8,(4,12,7))
  kamchatka = Country('kamchatka', my_map,9,9,(4,12,7))
  india = Country('india', my_map,7,5,(4,12,7))
  china = Country('china', my_map,8,6,(4,12,7))
  mongolia = Country('mongolia', my_map,9,7,(4,12,7))
  irkutsk = Country('irkutsk', my_map,8,8,(4,12,7))
  japan = Country('japan', my_map,9,8,(4,12,7))
  siam = Country('siam', my_map,8,5,(4,12,7))

  my_map.makeNeighbours(middle_east,egypt)
  my_map.makeNeighbours(middle_east,east_africa)
  my_map.makeNeighbours(middle_east,SEU)
  my_map.makeNeighbours(middle_east,ukraine)
  my_map.makeNeighbours(middle_east,afghanistan)
  my_map.makeNeighbours(middle_east,india)
  my_map.makeNeighbours(afghanistan,ukraine)
  my_map.makeNeighbours(afghanistan,ural)
  my_map.makeNeighbours(afghanistan,india)
  my_map.makeNeighbours(afghanistan,china)
  my_map.makeNeighbours(ural,ukraine)
  my_map.makeNeighbours(ural,siberia)
  my_map.makeNeighbours(ural,china)
  my_map.makeNeighbours(siberia,yakutsk)
  my_map.makeNeighbours(siberia,irkutsk)
  my_map.makeNeighbours(siberia,mongolia)
  my_map.makeNeighbours(siberia,china)
  my_map.makeNeighbours(yakutsk,irkutsk)
  my_map.makeNeighbours(irkutsk,kamchatka)
  my_map.makeNeighbours(irkutsk,mongolia)
  my_map.makeNeighbours(kamchatka,alaska)
  my_map.makeNeighbours(kamchatka,yakutsk)
  my_map.makeNeighbours(kamchatka,mongolia)
  my_map.makeNeighbours(kamchatka,japan)
  my_map.makeNeighbours(mongolia,japan)
  my_map.makeNeighbours(mongolia,china)
  my_map.makeNeighbours(china,india)
  my_map.makeNeighbours(china,siam)
  my_map.makeNeighbours(india,siam)

  #Australia
  indonesia = Country('indonesia', my_map,8,4,(5,4,2))
  new_guinea = Country('new_guinea', my_map,9,4,(5,4,2))
  western_australia = Country('western_australia', my_map,8,3,(5,4,2))
  eastern_australia = Country('eastern_australia', my_map,9,3,(5,4,2))

  my_map.makeNeighbours(indonesia,siam)
  my_map.makeNeighbours(indonesia,western_australia)
  my_map.makeNeighbours(indonesia,new_guinea)
  my_map.makeNeighbours(western_australia,new_guinea)
  my_map.makeNeighbours(western_australia,eastern_australia)
  my_map.makeNeighbours(eastern_australia,new_guinea)



  """
  ireland = Country('ireland', my_map,5,5,(1,2,3))
  scotland = Country('scotland',my_map,7,5,(0,2,10))
  wales = Country('wales',my_map,7,6,(2,2,3))
  france = Country('france',my_map,6,7,(2,2,3))
  england = Country('england', my_map,6,6,(0,2,10))
  ni = Country('NI', my_map,5,6,(1,2,3))
  """
  Country_list = my_map.nodes()
  """
  my_map.makeNeighbours(england,ireland)
  """
  
  index_list = [0,1,2,3,4,5]
  random.shuffle(index_list)
  counter = 0
  while counter < len(Country_list):
    
    if counter%len(index_list) == 0:
      random.shuffle(index_list)
    Player_list[index_list[counter%len(index_list)]].addCountry(Country_list[counter])
    
    counter += 1
    
  #Player1.addCountry(ireland)
  #Player1.addCountry(ni)
  #Player2.addCountry(england)
  #Player3.addCountry(scotland)
  #Player3.addCountry(wales)
  #Player2.addCountry(france)


  #for node in my_map.nodes():
  #  node.setSoldiers(random.randint(1,6))
  for i in range(5):
    for player in Player_list:
      player.place_random_soldier()

  return my_map



def build_simple_map():

  my_map = Map()
  Player1 = Player('ai_player', my_map)
  Player2 = Player('player2', my_map)
  Player3 = Player('player3', my_map)
  Player1.resetPlayerIndex()
  Player_list = my_map.getPlayerList()
  ireland = Country('ireland', my_map,5,5,(1,2,3))
  scotland = Country('scotland',my_map,7,5,(0,2,10))
  wales = Country('wales',my_map,7,6,(2,2,3))
  france = Country('france',my_map,6,7,(2,2,3))
  england = Country('england', my_map,6,6,(0,2,10))
  ni = Country('NI', my_map,5,6,(1,2,3))
  Country_list = my_map.nodes()
  my_map.makeNeighbours(england,ireland)
  my_map.makeNeighbours(ni,ireland)
  my_map.makeNeighbours(scotland,wales)
  my_map.makeNeighbours(england,wales)
  my_map.makeNeighbours(england,scotland)
  my_map.makeNeighbours(ireland,scotland)
  my_map.makeNeighbours(wales,france)
  #ireland.setRuler(Player1)
  index_list = [0,1,2]
  random.shuffle(index_list)
  counter = 0
  while counter < len(Country_list):
    if counter%len(index_list) == 0:
      random.shuffle(index_list)
    Player_list[index_list[counter%len(index_list)]].addCountry(Country_list[counter])
    counter += 1
    
  #Player1.addCountry(ireland)
  #Player1.addCountry(ni)
  #Player2.addCountry(england)
  #Player3.addCountry(scotland)
  #Player3.addCountry(wales)
  #Player2.addCountry(france)


  #for node in my_map.nodes():
  #  node.setSoldiers(random.randint(1,6))
  for i in range(8):
    for player in Player_list:
      player.place_random_soldier()

  return my_map