from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random

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

def reverse_direction(array):
    new_array = []
    for item in array:
        new_array.append(translate(item))
    return new_array

def decode(tiny_int):
    if tiny_int == 1:
        return 'n'
    elif tiny_int ==2:
        return 'e'
    elif tiny_int == 3:
        return 's'
    elif tiny_int ==4:
        return 'w'

def print_q_ids(q):
    q_ids = []
    for obj in q:
        q_ids.append(obj.id)
    print("queue ids", q_ids)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
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

def compute_path_to_terminal(starting_vertex, map, master_plan, terminal):
    # print("Current Room", current_room)
    traversal_path = []
    current_room = starting_vertex.id
    directions_by_room = map[terminal]
    directions_by_compass = []
    print(f"Directions by room to {terminal}", directions_by_room)
    for next_room in directions_by_room[1:]: # ex 7 8 
        for direction in master_plan[current_room]: # for n/s/e/w in {... 0: {'n': 1, 's': 5, 'w': 7, 'e': 3} ...}
            # print("current room", current_room,'next room', next_room,  "master plan[curent room]", master_plan[current_room], "Direction", direction)
            if master_plan[current_room][direction] == next_room: # if master_plan[0]['w'] == 7
                directions_by_compass.append(direction) # [].append('w')
                current_room = next_room
                break
    ruckwarts = reverse_direction(reversed(directions_by_compass))
    traversal_path = directions_by_compass
    traversal_path.extend(reverse_direction(directions_by_compass))
    print("directions by compass", directions_by_compass, "to room ", terminal)    

    print("directions by compass", directions_by_compass, "to room ", terminal)
    return traversal_path



def dfrandom(starting_vertex):   # depth first random
    master_plan[starting_vertex.id] = {}
    for exit in starting_vertex.get_exits():
        master_plan[starting_vertex.id][exit] = '?'
    print("master plan:", master_plan)    
    rand_dir = decode(random.randint(1,4))
    print("random dir", rand_dir)
        


    
dfrandom(world.starting_room)

traversal_path = []
# for terminal in terminal_list:
#     traversal_path.extend(compute_path_to_terminal(world.starting_room,room_map, master_plan, terminal))
# compute_path_to_terminals(world.starting_room,room_map, master_plan, terminal_list)
print("final traversal path", traversal_path)
# traversal_path = tuple_return[0]
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    # print("------------------\ncurrent room", player.current_room, '\n------------------\n--------------------')
    # print("Current room exits:", player.current_room.get_exits())
    # print("Current room exits string:", player.current_room.get_exits_string())
    # print("Current room desc:", player.current_room.description)
    visited_rooms_printer = set()
    for room in visited_rooms:
        visited_rooms_printer.add(room.id)
    # print('visited rooms', visited_rooms_printer)

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
