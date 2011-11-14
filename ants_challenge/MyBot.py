#!/usr/bin/env python
from ants import *
from decimal import *
import logging

class MyBot:
    DIRECTIONS = ('n','w','s','e')
    ATTACK, FOOD, SCOUT, EVADE_FRIENDLY_HILL, EVADE_FRIENDLY_ANT = (0, 1, 2, 3, 4)

    def __init__(self):
        logging.basicConfig(filename='mybot.log',level=logging.DEBUG)

    def do_setup(self, ants):
        self.init_world(ants)

    def init_world(self, ants):
	self.world = {}

        for x in range(ants.cols):
            for y in range(ants.rows):
                self.world[(y, x)] = {}

		if (not ants.passable((y, x))):
			val = -1
		else:
			val = 0

                self.world[(y, x)][MyBot.ATTACK] = val
                self.world[(y, x)][MyBot.FOOD] = val
                self.world[(y, x)][MyBot.SCOUT] = val
                self.world[(y, x)][MyBot.EVADE_FRIENDLY_HILL] = val
                self.world[(y, x)][MyBot.EVADE_FRIENDLY_ANT] = val

    def update_world_food(self, ants, val):
        for food_loc in ants.food():
            self.diffuse(ants, food_loc, MyBot.FOOD, val)

    def evade_friendly_hills(self, ants, val):
        for hill_loc in ants.my_hills():
            self.diffuse(ants, hill_loc, MyBot.EVADE_FRIENDLY_HILL, val)

    def evade_friendly_ants(self, ants, val):
        for hill_loc in ants.my_ants():
            self.diffuse(ants, hill_loc, MyBot.EVADE_FRIENDLY_ANT, val)

    def diffuse(self, ants, source, goal, score):
        open_nodes = []
	open_set = set()
        closed_set = set()
        distances = {}
        
        distances[source] = 0
        open_set.add(source)
        open_nodes.append(source)

        current_score = score
        
        while (len(open_nodes) > 0):
            current_node = open_nodes[0]

            if (distances[current_node] > 25):
                break

            open_set.remove(current_node)
            open_nodes.remove(current_node)
            closed_set.add(current_node)
            current_score = score / (distances[current_node] + 1)
            self.world[current_node][goal] += current_score

            for direction in MyBot.DIRECTIONS:
                destination = ants.destination(current_node, direction)

                if ants.passable(destination) and (destination not in closed_set) and (destination not in open_set):
                    distances[destination] = distances[current_node] + 1
                    open_nodes.append(destination)
                    open_set.add(destination)

    def do_turn(self, ants):
        logging.info("Starting turn!")
        self.init_world(ants)
        self.update_world_food(ants, 1024)
        self.evade_friendly_hills(ants, -20)
        self.evade_friendly_ants(ants, -10)
        
        all_orders = []
        
        for ant in ants.my_ants():
            best_direction = MyBot.DIRECTIONS[0]
            best_value = -1
            for direction in MyBot.DIRECTIONS:
                destination = ants.destination(ant, direction)

                if (self.world[destination][MyBot.FOOD] > best_value):
                    best_value = self.world[destination][MyBot.FOOD] + self.world[destination][MyBot.ATTACK] + self.world[destination][MyBot.SCOUT] + self.world[destination][MyBot.EVADE_FRIENDLY_HILL] + self.world[destination][MyBot.EVADE_FRIENDLY_ANT]
                    best_direction = direction

            all_orders.append((ant, best_direction))
            
                
        #Ignore duplicate orders (different ants ordered to the same location and multiple orders to same ant)
        new_locations = set()
        
        for order in all_orders:
            destination = ants.destination(order[0], order[1])
            
            if (not destination in new_locations):
                new_locations.add(destination)
                ants.issue_order((order[0], order[1]))

	logging.info("Turn ended!")

    def pprint(self, ants, world_dict, order):
        txt = "\n"
        for y in range(ants.cols):
            for x in range(ants.rows):
                txt += str(world_dict[(x, y)][order]) + "\t"
            txt += "\n"

        txt += "\n"
            
        return txt

if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
