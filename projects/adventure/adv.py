from room import Room
from player import Player
from world import World
from util import Stack, Queue  

import random
from ast import literal_eval

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


def bft(starting_vertex):
    """
    Print each vertex in breadth-first order
    beginning from starting_vertex.
    """
    # create empty queue
    counter = 1
    q = []
    # ceate set to store visited nodes
    visited = set()
    traversal_path = []
    master_plan[starting_vertex.id] = starting_vertex.get_exits()
    print("Master plan", master_plan)
    # initialize starting note
    q.append(starting_vertex)
    # while queue isn't empty
    while len(q) > 0:

        print("counter: ", counter)
        counter += 1
        q_ids = []
        for i in q:
            q_ids.append(i.id)
        # dequeue first item
        # print("q[0] id:", q[0].id)
        v_obj = q.pop()
        print("queue ids", q_ids)

        if v_obj.id not in master_plan:
            master_plan[v_obj.id] = v_obj.get_exits()
            print("master plan", master_plan)        


        if v_obj.id not in visited:
            visited.add(v_obj.id)
            # print('visited', visited)
            # Do something with node
            # add all neighbors to queue
        # elif v in visited:
            # instruct it to not return whence it came somehow
            for direction in v_obj.get_exits():  # This is doing it too fast. Getting them all at once. Have to go back to queue after having gotten one. Have to call queue. 
                traversal_path.append(direction)
                print('v_obj id:', v_obj.id)
                print('v_obj get exits:', v_obj.get_exits())
                print("Traversal Path", traversal_path)
                # print("direction", direction)
                next_room = v_obj.get_room_in_direction(direction)
                q.append(next_room)
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
