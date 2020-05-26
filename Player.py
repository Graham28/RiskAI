import copy
import random
class Player:

  player_index = 0
  #initilize player class
  def __init__(self, name, game_map, countries = None):
    if countries:
      self.countries = countries
    else:
      self.countries = []
    self.name = name
    self.map = game_map
    self.index = copy.deepcopy(Player.player_index)
    Player.player_index += 1
    self.map.addPlayer(self)
    self.continents_dict = {}
    self.num_soldiers = 0


  def resetPlayerIndex(self):
    Player.player_index = 0
    
  def attack(self,attack_from, victim):
    #print(self.name + ' attacked ' + victim.getRuler().getName() + ' in ' + victim.getName() + '.')
    num_victim = victim.getSoldiers()
    if num_victim > attack_from.getSoldiers() - 1:
      victim.setSoldiers(num_victim-(attack_from.getSoldiers()-1))
      attack_from.setSoldiers(1)
      #print('The attack did not succeed.')
    elif num_victim < attack_from.getSoldiers() - 1:
      victim.getRuler().removeCountry(victim)
      if len(victim.getRuler().getCountries()) == 0:
        self.map.removePlayer(victim.getRuler())
      victim.setRuler(self)
      victim.setSoldiers((attack_from.getSoldiers() - 1)-int(num_victim*0.7))
      attack_from.setSoldiers(1)
      self.addCountry(victim)
      #print(self.name + ' now has control over ' + victim.getName() + '.')

    else:
      victim.getRuler().removeCountry(victim)
      
      if len(victim.getRuler().getCountries()) == 0:
        self.map.removePlayer(victim.getRuler())

      victim.setRuler(self)
      victim.setSoldiers(1)
      attack_from.setSoldiers(1)
      self.addCountry(victim)
      #print(self.name + ' now has control over ' + victim.getName() + '.')

  def update_num_soldiers(self):
    old_value = copy.deepcopy(self.num_soldiers)
    self.num_soldiers = self.get_num_soldiers()

    return self.num_soldiers - old_value
  
  def get_num_soldiers(self):
    num = 0
    for country in self.countries:
      num += country.getSoldiers()

    return num

  def calc_reward(self):
    reward = 3
    continent_list_keys = self.continents_dict.keys()
    for key in continent_list_keys:
      if self.continents_dict[key] == key[1]:
        reward += copy.deepcopy(key[2])
    
    return reward

  def place_reward_random(self):
    x = random.randint(0,len(self.countries)-1)

    self.countries[x].setSoldiers(self.countries[x].getSoldiers() + self.calc_reward())



  def random_attack(self):
    for c in self.countries:
      neighbours = c.getNeighbours()
      for n in neighbours:
        if n.getRuler() != self and c.getSoldiers() > n.getSoldiers():
          self.attack(c,n)
          return [c,n] 

  def fortify(self):
    finished = False
    #loop through countries
    for c in self.countries:
      if finished:
        break
      #if the country doesn't have an enemy neighbour and has more than 1 soldier
      if not c.getEnemyNeighbour() and c.getSoldiers() > 1:
        #loop through it's neighbours
        for n in c.getNeighbours():
          #if this neighbour has an enemy neighbour
          if n.getEnemyNeighbour():
            #fortify to here, and break loops
            n.setSoldiers(n.getSoldiers() + c.getSoldiers() -1)
            c.setSoldiers(1)
            finished = True
            break
  
  def takeRandomTurn(self):
    self.random_attack()
    self.fortify()

  def addCountry(self, country):
    if country not in self.countries:
      self.countries.append(country)
    if country.getContinent() in self.continents_dict:
      self.continents_dict[country.getContinent()] += 1
    else:
      self.continents_dict[country.getContinent()] = 1
    country.setRuler(self)
  def removeCountry(self, country):
    self.countries.remove(country)
    self.continents_dict[country.getContinent()] -=1

  def getCountries(self): return self.countries

  def getName(self): return self.name

  def getIndex(self): return self.index

  #edits the print function
  """
  def __str__(self):
    country_string = ''
    for c in self.countries:
      country_string += c.getName() + ' '
    return str(self.name) + ' ' + country_string
   """