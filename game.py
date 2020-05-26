from Country import Country
from Map import Map
from Player import Player
from functions import *

simple_map = Map()

Player1 = Player('player1', simple_map)
Player2 = Player('player2', simple_map)

ireland = Country('ireland', simple_map)
england = Country('england',simple_map)
northern_ireland = Country('NI', simple_map)

newRulerOfCountry(Player1,ireland,10)

newRulerOfCountry(Player1, northern_ireland,4)

newRulerOfCountry(Player2,england,5)



simple_map.add_node(ireland)
simple_map.add_node(northern_ireland)
simple_map.add_node(england)
simple_map.makeNeighbours(ireland, england)
simple_map.makeNeighbours(ireland, northern_ireland)

print(ireland)
print(england)
print(northern_ireland)

Player1.fortify()

print(ireland)
print(england)
print(northern_ireland)
