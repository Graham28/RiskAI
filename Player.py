import copy
import random
class Player:

  player_index = 0
  #initilize player class
  def __init__(self, name, game_map, randomness, countries = None):
    if countries:
      self.countries = countries
    else:
      self.countries = []
    self.name = name
    self.map = game_map
    self.randomness = randomness
    self.index = copy.deepcopy(Player.player_index)
    Player.player_index += 1
    self.map.addPlayer(self)
    self.continents_dict = {}
    self.num_soldiers = 0
    self.attacked_last_move = False #has to be a successful attack
    self.cards = 0


  def resetPlayerIndex(self):
    Player.player_index = 0
    
  def attack(self,attack_from, victim):
    #print(self.name + ' attacked ' + victim.getRuler().getName() + ' in ' + victim.getName() + '.')
    if attack_from.getRuler() != self or victim.getRuler() ==self:
      return [attack_from,victim]
    num_victim = victim.getSoldiers()
    if num_victim > attack_from.getSoldiers() - 1:
      victim.setSoldiers(num_victim-(attack_from.getSoldiers()-1))
      attack_from.setSoldiers(1)
      #print('The attack did not succeed.')
    elif num_victim < attack_from.getSoldiers() - 1:
      victim.getRuler().removeCountry(victim)
      self.attacked_last_move = True
      if len(victim.getRuler().getCountries()) == 0:
        self.map.removePlayer(victim.getRuler())
        #print('DIED')
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
    
    return [attack_from,victim]

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
    if self.attacked_last_move:
      reward = 3
      self.cards += 1
    else:
      reward = 0
      self.cards = 0
    if self.cards == 3:
      reward += 7
      self.cards = 0

    continent_list_keys = self.continents_dict.keys()
    for key in continent_list_keys:
      if self.continents_dict[key] == key[1]:
        reward += copy.deepcopy(key[2])
    
    return reward

  def place_reward_random(self):
    draft_list = []
    for i in self.countries:
      if i.getEnemyNeighbour():
        draft_list.append(i)
    x = random.randint(0,len(draft_list)-1)

    self.countries[x].setSoldiers(draft_list[x].getSoldiers() + self.calc_reward())

    return self.countries[x]
  
  def place_random_soldier(self):
    x = random.randint(0,len(self.countries)-1)

    self.countries[x].setSoldiers(self.countries[x].getSoldiers() + 1)



  def random_attack(self):
    attack_list = []
    for c in self.countries:
      neighbours = c.getNeighbours()
      for n in neighbours:
        if n.getRuler() != self and c.getSoldiers() > 1:
          attack_list.append([c,n])
    if len(attack_list) == 0:
      return None
    else:
      x = random.randint(0, len(attack_list)-1)
      self.attack(attack_list[x][0],attack_list[x][1])
      if random.randint(0,1) == 1:
        self.random_attack()
      return attack_list[x] 

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

  def fortify_random(self):
    fortify_list = []
    for c in self.countries:
      for n in self.countries:
        #if n != c and self.is_connected(n,c):
        if n != c:
          fortify_list.append([c,n])
    
    if len(fortify_list) > 0:
      chosen_pair = fortify_list[random.randint(0,len(fortify_list)-1)]
      if self.is_connected(chosen_pair[0],chosen_pair[1]):
        self.fortify_(chosen_pair[0],chosen_pair[1])
      return chosen_pair
    else:
      return

  def fortify_(self,country1,country2):
    country1.setSoldiers(country1.getSoldiers() + country2.getSoldiers() - 1)
    country2.setSoldiers(1)
    return [country1,country2]

  def is_connected(self, country1, country2):
    """
    """
    assert self.map.has_node(country1)
    if country1.getRuler() != self:
      return False
    # visited list
    visited = []
    # Keep the nodes yet to visit in another list, used as a queue.
    # Initially, only the country1 node is to be visited.
    to_visit = [country1]
    # While there are nodes to be visited:
    while to_visit != []:
        # Visit the next node at the front of the queue.
        next_node = to_visit.pop(0)
        visited.append(next_node)
        # Look at its neighbours.
        for neighbour in self.map.neighbours(next_node):
            # Add node to the back of the queue if not already
            # visited or not already in the queue to be visited.
            if neighbour == country2 and neighbour.getRuler() == self:
              return True
            elif (neighbour not in visited and neighbour not in to_visit) and neighbour.getRuler() == self:
                to_visit.append(neighbour)
    return False

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

  def getRandomness(self): return self.randomness

  #edits the print function
  
  def __str__(self):
    country_string = ''
    for c in self.countries:
      country_string += c.getName() + ' '
    return str(self.name) + ' ' + country_string
  