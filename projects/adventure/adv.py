from room import Room
from player import Player
from world import World
from util import Stack, Queue  

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
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


def bft(starting_vertex):
    """
    Print each vertex in breadth-first order
    beginning from starting_vertex.
    """
    # create empty queue
    q = Queue()
    # ceate set to store visited nodes
    traversal_list = set()
    visited = set()  
    # initialize starting note
    q.enqueue(starting_vertex)
    # while queue isn't empty
    while q.size() > 0:
        # dequeue first item
        v = q.dequeue()

        if v not in visited:
            visited.add(v)
            # Do something with node
            print(f'{v}')
            # add all neighbors to queue
            print('v value:', v)
            for next_vert in v.get_exits():  # Need to find the get neighbors function
                q.enqueue(next_vert)

    return visited

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
    print("Current room exits:", player.current_room.get_exits())
    print("Current room exits string:", player.current_room.get_exits_string())
    print("Current room desc:", player.current_room.description)
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
