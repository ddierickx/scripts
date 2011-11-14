import math
import logging
import Queue

# Perform a-star search
def get_path(graph, start_loc, end_loc):
    def h_to_goal(loc):
        return h(loc, end_loc)
    def h(s_loc, e_loc):
        return math.fabs(s_loc[0] - e_loc[0]) + math.fabs(s_loc[1] - e_loc[1])
    def g(loc):
        if (loc not in g_scores):
            return float('inf')
        else:
            return g_scores[loc]
    def f(loc):
        return h_to_goal(loc) + g(loc)
    def expand(loc):
        neighbours = [ (loc[0] - 1, loc[1] + 0),
                       (loc[0] + 1, loc[1] + 0),
                       (loc[0] + 0, loc[1] - 1),
                       (loc[0] + 0, loc[1] + 1) ]
        return filter(lambda x: passable(loc), neighbours)
    
    def passable(loc):
        val = (loc[0] < len(graph)) and (loc[0] >= 0) and (loc[1] < len(graph[loc[0]]) and (loc[1] >= 0)) and (graph[loc[0]][loc[1]] == 0)
        print str(loc) + " is passable " + str(val)
        return val
        
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

    weights = graph[:]
    open_q = Queue.PriorityQueue()
    open_s = set()
    closed_s = set()

    # No need to calculate initial heuristic since it will always be picked and removed
    open_q.put((0, start_loc))
    open_s.add(start_loc)
    g_scores[start_loc] = 0

    while (len(open_s) != 0):
        best_loc = open_q.get()[1]
        
        if (best_loc == end_loc):
            path = reconstruct_path()
            return path, g_scores
        
        closed_s.add(best_loc)
        open_s.remove(best_loc)
        
        #expand best_loc
        for neighbour_loc in expand(best_loc):
            if (neighbour_loc in closed_s):
                continue

            if (neighbour_loc not in open_s):
                g_scores[neighbour_loc] = g_scores[best_loc] + h(best_loc, neighbour_loc)
                open_q.put((f(neighbour_loc), neighbour_loc))
                open_s.add(neighbour_loc)
                backtrack[neighbour_loc] = best_loc
            else:
                # Found shorter path to reach neighbour?
                tentative_g = g(best_loc) + h(best_loc, neighbour_loc)
                is_better_g = (tentative_g > g(neighbour_loc))

                if (is_better_g):
                    backtrack[neighbour_loc] = best_loc
                    g_scores[neighbour_loc] = tentative_g
    #No path found
    logging.warning("No path found from " + str(start_loc) + " to " + str(end_loc))
    return None, g_scores

def pprint(graph):
    for row in graph:
        for rowcol in row:
            print rowcol,
        print ""

graph = [x for x in range(0, 10)]
graph[0] = [0,0,0,0,0,0,0,0,0,0]
graph[1] = [0,0,0,0,0,0,0,0,0,0]
graph[2] = [0,1,1,0,0,0,0,0,0,0]
graph[3] = [0,0,1,1,1,0,0,0,0,0]
graph[4] = [0,0,0,0,0,0,0,0,0,0]
graph[5] = [0,0,0,0,0,1,1,1,1,1]
graph[6] = [0,0,0,0,0,0,0,0,0,0]
graph[7] = [1,1,1,1,1,0,0,0,0,0]
graph[8] = [0,0,0,0,0,0,1,1,0,0]
graph[9] = [0,0,0,0,0,0,0,0,0,0]

path, g_scores = get_path(graph, (0, 0), (9, 9))

for node in path:
    graph[node[0]][node[1]] = "*"

scores = graph[:]

print g_scores

for score in g_scores.keys():
    print score[0]
    print score[1]
    print "--"
    scores[score[0]][score[1]] = g_scores[score]

pprint(graph)
