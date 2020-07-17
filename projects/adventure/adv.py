from room import Room
from player import Player
from world import World
from util import Stack, Queue  

import random
from ast import literal_eval

def translate(dir):
    if dir == "s":
        return "n"
    elif dir == 'n':
        return 's'
    elif dir == 'e':
        return 'w'
    elif dir == 'w':
        return 'e'
    else:
        return

def print_q_ids(q):
    q_ids = []
    for obj in q:
        q_ids.append(obj.id)
    print("queue ids", q_ids)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# print('starting room---', world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n', 'n']
traversal_path = []
master_plan = {}

def back_peddle(room, master_plan):
    if room.id in master_plan:
        print(room.id)



def bft(starting_vertex):

    q = []
    visited = set()
    traversal_path = []
    master_plan[starting_vertex.id] = {}
    for exit in starting_vertex.get_exits():
        master_plan[starting_vertex.id][exit] = '?'



    # initialize starting note
    q.append(starting_vertex)

    while len(q) > 0:
        # print_q_ids(q)
        v_obj = q.pop()

        # Init room in master plan
        if v_obj.id not in master_plan:
            master_plan[v_obj.id] = {}
            for exit in v_obj.get_exits():
                master_plan[v_obj.id][exit] = '?'
        

        # Populate visited. Not going to be as important for this exercise however, but add it to log. 
        if v_obj.id not in visited:
            visited.add(v_obj.id)
            print('visited', visited)

        # instruct it to not return whence it came somehow
        for direction in v_obj.get_exits():
            next_room = v_obj.get_room_in_direction(direction) # This is effectivelhy moving
            
            master_plan[v_obj.id][direction] = next_room.id
            if next_room.id not in master_plan:
                master_plan[next_room.id] = {}
                for exit in next_room.get_exits():
                    master_plan[next_room.id][exit] = '?'
            
            master_plan[next_room.id][translate(direction)] = v_obj.id; print("master plan coming together", master_plan)
            q.append(next_room)
            traversal_path.append(direction)
    print("final rooms visited", visited)
    return traversal_path

traversal_path = bft(world.starting_room)
print("Traversal Path:", traversal_path)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    print("------------------\ncurrent room", player.current_room, '\n------------------\n--------------------')
    # print("Current room exits:", player.current_room.get_exits())
    # print("Current room exits string:", player.current_room.get_exits_string())
    # print("Current room desc:", player.current_room.description)
    visited_rooms_printer = set()
    for room in visited_rooms:
        visited_rooms_printer.add(room.id)
    print('visited rooms', visited_rooms_printer)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
