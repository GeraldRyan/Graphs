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
def mirror(dir):
    if dir == 's':
        return 'n'
    elif dir =='w':
        return 'e'
    elif dir == 'n':
        return 's'
    elif dir =='e':
        return 'w'
    else:
        return False
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
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
directions_to_room_x = {} # Do we need this now?
visited_rooms = set()
visited_rooms.add(world.starting_room)
df_room_traversal_path = []

# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.

# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a `'?'` for an exit. If you use the `bfs` code from the homework, you will need to make a few modifications.

# 1. Instead of searching for a target vertex, you are searching for an exit with a `'?'` as the value. If an exit has been explored, you can put it in your BFS queue like normal.

# 2. BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.

# If all paths have been explored, you're done!


current_room = world.starting_room
def draw_master_plan(v, dir=None, new_room=None):
    if v.id not in master_plan:
        exits = v.get_exits() 
        master_plan[v.id] = {}
        for exit in exits:
            master_plan[v.id][exit] = "?"
    elif dir is not None and new_room is not None:
        master_plan[v.id][dir] = new_room.id
        try:
            master_plan[new_room.id][mirror(dir)] = v.id
        except:
            master_plan[new_room.id] = {}
            master_plan[new_room.id][mirror(dir)] = v.id
    
def dfrandom(starting_vertex=world.starting_room):
    global current_room
    # might have to make the globals into localsand return them, so I can run this recursively
    s = Stack()
    s.push(starting_vertex)
    visited = set()
    df_dir_traversal_path = []

    while s.size() > 0:
        v = s.pop()
        if v not in visited:
            visited.add(v)
            draw_master_plan(v)
            exits = v.get_exits()
            df_room_traversal_path.append(v.id)
            # print('all exits', exits)
            if len(exits) == 1 and v.id !=0: # if it's a terminal room but not the beginning
                return df_dir_traversal_path
            # take away the mirror of the exit so that if they just went north, then south is out of the list
            if 'random_exit' in locals():
                exits.remove(mirror(random_exit))
            # print('allowed exits', exits)
            random_exit = random.choice(exits)
            new_room = v.get_room_in_direction(random_exit)
            if new_room.id != 0:
                df_dir_traversal_path.append(random_exit)
            current_room = v # hoist new room to global scope
            print("current room", current_room.id)
            print('new room, looking for zero', new_room.id)
            draw_master_plan(v, random_exit, new_room)
            s.push(new_room)
            if new_room.id == 0:
                draw_master_plan(v, random_exit, new_room)
                print("master plan finished", master_plan)
                return df_dir_traversal_path
    print("depth first room traversal path", df_room_traversal_path)

    return df_dir_traversal_path


traversal_path = dfrandom()
print("depth first direction traversal path", traversal_path)
print("depth first room traversal path", df_room_traversal_path)
place_on_path = len(traversal_path) - 1
print("place on path", place_on_path)

print("Current Room:", current_room.id, "master Plan:", master_plan)
print("mirror traversal_path[place_on_path]",mirror(traversal_path[place_on_path]))

def backtrack():

    while '?' not in master_plan[current_room.id].values():
        prior_room = current_room.get_room_in_direction(traversal_path[place_on_path])
        print("While loop running")
    print("While loop just ran")
    print("current room", current_room.id, master_plan[current_room.id].values())

        
backtrack()

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
