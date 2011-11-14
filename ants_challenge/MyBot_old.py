#!/usr/bin/env python
from ants import *
import logging
import Queue

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    DIRECTIONS = ('n','w','s','e')
    GATHERERS_BEFORE_ATTACKERS = 2
    ATTACKER, GATHERER, SCOUTER = (0, 1, 2)

    def get_active_path(self, ant_loc):
        for distance_path_pair in self.active_paths:
            path = distance_path_pair[2]

            if (path[0] == ant_loc):
                return distance_path_pair
            else:
                return None

    def resume_active_path(self, ants):
        remaining_ants = []
        orders = []

        for path in self.active_paths:
            logging.debug("S:" + str(path[0]) + " P: " + str(path[2]))

        for ant_loc in ants.my_ants():
            current_path = self.get_active_path(ant_loc)

            if (current_path == None):
                remaining_ants.append(ant_loc)
                pass
            else:
                start_loc = current_path[0]
                distance = current_path[1]
                remaining_path = current_path[2]            
                logging.debug("LOP: " + str(len(remaining_path)))
                if (len(remaining_path) == 2):
                    # Last move, give last order and remove
                    orders.append((ant_loc, ants.direction(remaining_path[0], remaining_path[1])[0]))
                    self.active_paths.remove(current_path)
                    logging.debug("Path has ended at: " + str(remaining_path[1]))
                elif (len(remaining_path) > 2):
                    # Not the last order, move to next
                    direction = ants.direction(remaining_path[0], remaining_path[1])[0]
                    orders.append((ant_loc, direction))
                    self.activate_path(ants, start_loc, remaining_path[1:])
                    logging.debug("Path has continued to: " + str(remaining_path[1]))
                else:
                    # This shouldn't happen (len == 0)
                    logging.debug("Zero length path detected")
                    self.active_paths.remove(current_path)
                    remaining_ants.append(ant_loc)

        return remaining_ants, orders
                    
                    
    def __init__(self):
        # define class level variables, will be remembered between turns
        logging.basicConfig(filename='mybot.log',level=logging.DEBUG)
        self.enemy_hills = set()
        self.unseen = []
        # list (start_loc, remaining_locs, current_loc + remaining_path]
        self.active_paths = []

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))

    def discover_enemy_pits(self, ants):
        for hill in ants.enemy_hills():
            logging.warning("Enemy hill discovered: " + str(hill))
            self.enemy_hills.add(hill)

    def update_los(self, ants):
        for loc in self.unseen[:]:
            if ants.visible(loc):
                self.unseen.remove(loc)
    
    def get_scout_orders(self, ants, ants_awaiting_orders):
        def get_los_invisible_neighbours(unseen_loc):
            pass            
        
        orders = []
        being_scouted = set()

        for ant_loc in ants_awaiting_orders:
            closest_undiscovered = min(map(lambda unseen_loc: (ants.distance(ant_loc, unseen_loc), unseen_loc),
                                               filter(lambda loc:(ants.passable(loc)) and (loc not in being_scouted), self.unseen)))
            path = self.get_path(ants, ant_loc, closest_undiscovered[1])
            being_scouted.add(closest_undiscovered)
            logging.debug("Scout " + str(ant_loc) + " will scout " + str(closest_undiscovered) + " via " + str(path))
            self.activate_path(ants, ant_loc, path)

        return [], orders

    def activate_path(self, ants, start_loc, path):
        # Replace paths with new orders
        order = self.get_active_path(start_loc)
        if (order != None):
            self.active_paths.remove(order)
        self.active_paths.append((start_loc, len(path), path))

    def get_gather_orders(self, ants, ants_awaiting_orders):
        orders = []
        
        closest_ant_to_food = {}
        ant_to_food_paths = {}
        ants_without_orders = []
        ants_without_orders.extend(ants_awaiting_orders)
        
        for food_loc in ants.food():
            min_distance = float('inf')
            ant_to_food_path = {}
            
            for ant in ants_awaiting_orders:
                path = self.get_path(ants, ant, food_loc)
                ant_to_food_path[ant] = path
                
                if (len(path) < min_distance):
                    closest_ant_to_food[food_loc] = ant
                    min_distance = len(path)

            ant_to_food_paths[food_loc] = ant_to_food_path
            
        for food_loc in ants.food():
            try:
                nearest_ant = closest_ant_to_food[food_loc]
                self.activate_path(ants, nearest_ant, ant_to_food_paths[food_loc][nearest_ant])
                logging.debug("Gatherer " + str(nearest_ant) + " will gather food at " + str(food_loc))
                ants_without_orders.remove(nearest_ant)
            except:
                #ignore keyerror on duplicate remove...
                pass

        return (ants_without_orders, orders)
        
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        logging.info("Starting turn!")
        logging.debug("Active paths: " + str(len(self.active_paths)))
        logging.debug("Ants: " + str(len(ants.my_ants())))
        #logging.debug(str(self.get_passable_neighbours(ants, ants.my_hills()[0], 1)))
        all_orders = []

        self.update_los(ants)
        self.discover_enemy_pits(ants)

        # Resume paths of ants on path to scout location or food
        ants_that_dont_have_paths, resume_path_orders = self.resume_active_path(ants)
        logging.debug("Ants without paths: " + str(len(ants_that_dont_have_paths)))
        ants_that_dont_gather, gather_orders = self.get_gather_orders(ants, ants_that_dont_have_paths)

        # Ants not near food become scouts
        ants_that_dont_scout, scout_orders = self.get_scout_orders(ants, ants_that_dont_gather)

        all_orders.extend(resume_path_orders)
        #all_orders.extend(scout_orders)
        #all_orders.extend(gather_orders)

        for order in resume_path_orders:
            logging.debug("Follow " + str(order[0]) + " to " + str(order[1]))
        
        new_locations = set()
        ants_with_orders = set()
        
        #Ignore duplicate orders (different ants ordered to the same location and multiple orders to same ant)
        for order in all_orders:
            destination = ants.destination(order[0], order[1])
            
            if (not destination in new_locations) and (not order[0] in ants_with_orders):
                new_locations.add(destination)
                ants.issue_order((order[0], order[1]))
                ants_with_orders.add(order[0])

    # Perform a-star search
    def get_path(self, ants, start_loc, end_loc):
        def h(loc):
            return ants.distance(loc, end_loc)
        def g(loc):
            if (loc not in g_scores):
                return float('inf')
            else:
                return g_scores[loc]
        def f(loc):
            return h(loc) + g(loc)
        def expand(loc):
            neighbours = []
            for direction in MyBot.DIRECTIONS:
                new_destination = ants.destination(loc, direction)
                if (ants.passable(new_destination)):
                    neighbours.append(new_destination)
            return neighbours
            
        def reconstruct_path():
            current_loc = end_loc
            path = []
            
            while (current_loc in backtrack):
                next_loc = backtrack[current_loc]
                path.insert(0, current_loc)
                current_loc = next_loc

            path.insert(0, start_loc)

            return path
        
        backtrack = {}
        g_scores = {}
        
        open_q = Queue.PriorityQueue()
        open_s = set()
        closed_s = set()

        #No need to calculate initial heuristic since it will always be picked and removed
        open_q.put((0, start_loc))
        open_s.add(start_loc)
        g_scores[start_loc] = 0

        while (len(open_s) != 0):
            best_loc = open_q.get()[1]
            
            if (best_loc == end_loc):
                path = reconstruct_path()
                return path
            
            closed_s.add(best_loc)
            open_s.remove(best_loc)
            
            #expand best_loc
            for neighbour_loc in expand(best_loc):
                if (neighbour_loc in closed_s):
                    continue

                if (neighbour_loc not in open_s):
                    g_scores[neighbour_loc] = g_scores[best_loc] + ants.distance(best_loc, neighbour_loc)
                    open_q.put((h(neighbour_loc), neighbour_loc))
                    open_s.add(neighbour_loc)
                    backtrack[neighbour_loc] = best_loc
                else:
                    # Found shorter path to reach neighbour?
                    tentative_g = g(best_loc) + ants.distance(best_loc, neighbour_loc)
                    is_better_g = (tentative_g > g(neighbour_loc))

                    if (is_better_g):
                        backtrack[neighbour_loc] = best_loc
                        g_scores[neighbour_loc] = tentative_g

        #No path found
        logging.warning("No path found from " + str(start_loc) + " to " + str(end_loc))
        return None

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
