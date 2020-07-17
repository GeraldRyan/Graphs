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
visited_rooms = set()
visited_rooms.add(world.starting_room)
    
def dfrandom(starting_vertex=world.starting_room):
    dftravel_path = []
    rand_room = random.randint(1, len(room_graph))
    s = Stack()
    visited = set()
    s.push(starting_vertex)
    while s.size() >0:
        v = s.pop()
        exits = v.get_exits()
        print('exits', exits)
        if len(exits) != 1:
            if v not in visited:
                visited.add(v)
                new_room = v.get_room_in_direction(decode(random.randint(1, len(exits))))
                print('new room', new_room.id)
                exits = new_room.get_exits()
                s.push(new_room)
                print('exits', exits)
        else: 
            
        
    
    return dftravel_path

df_traversal_path = dfrandom()








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
