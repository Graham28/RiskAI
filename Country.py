class Country:

  #initilize country class
  def __init__(self, name, game_map, x, y, continent, soldiers = 1, neighbours = None, ruler = None):
    self.name = name
    self.soldiers = soldiers
    if neighbours:
      self.neighbours = neighbours
    else:
      self.neighbours = []
    self.ruler = ruler
    self.game_map = game_map
    self.continent = continent #tuple (index, num_countries)
    self.x = x
    self.y = y
    self.game_map.addCountry(self)


  def getFriendlyNeighbour(self):
    for n in self.neighbours:
      if n.getRuler() == self.getRuler():
        return n
      
    return False
  
  def getEnemyNeighbour(self):
    for n in self.neighbours:
      if n.getRuler() != self.getRuler():
        return n
    return False
    
  #getter and setters
  def getName(self): return self.name
  def getSoldiers(self): return self.soldiers
  def getNeighbours(self): return self.neighbours
  def getRuler(self): return self.ruler
  def getMap(self): return self.game_map
  def getContinent(self): return self.continent
  def getX(self): return self.x
  def getY(self): return self.y
  def setSoldiers(self, num_soldiers): self.soldiers = num_soldiers
  def addNeighbour(self, neighbours):
    self.neighbours.append(neighbours)
  def setRuler(self, new_ruler): self.ruler = new_ruler

  #edits the print function
  def __str__(self):
    neighbour_string = ''
    for n in self.neighbours:
      neighbour_string += n.getName() + ' '
    return self.name + ': Ruler is ' + str(self.ruler.getName()) + ', neighbours are ' + neighbour_string + ', number of soldiers is ' + str(self.soldiers)