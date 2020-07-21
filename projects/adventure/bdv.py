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
    s = Stack()
    s.push(starting_vertex)
    visited = set()
    df_dir_traversal_path = []

    while s.size() > 0:  # Get rid of while loop
        v = s.pop()
        if v not in visited:
            visited.add(v)
            draw_master_plan(v)
            exits = v.get_exits()
            df_room_traversal_path.append(v.id)
            # print('all exits', exits)
            if len(exits) == 1: # if it's a terminal room but not the beginning
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
# place_on_path = len(traversal_path) - 1
# print("place on path", place_on_path)

print("Current Room:", current_room.id, "master Plan:", master_plan)
# print("mirror traversal_path[place_on_path]",mirror(traversal_path[place_on_path]))

def bfs(starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    # Create an empty queue and enqueue A PATH TO the starting vertex ID
    q = Queue()
    q.enqueue([starting_vertex])
    print("check 1, starting vertex", starting_vertex)
    print("Check 2, q size", q.size())
    # Create a Set to store visited vertices
    visited = set()  
    # While the queue is not empty...
    while q.size() > 0:
        # Dequeue the first PATH
        path = q.dequeue()
        # Grab the last vertex from the PATH
        v = path[-1]
        # print("Spacer and path", path[-1].id)
        # If that vertex has not been visited...
        # print(f"v.id and visited {v.id},  {visited}")
        if v.id not in visited: # THis is where the error is coming from. It is not running this line because it's visited but running prior. So it's not queueing up right I think. `` 
            # CHECK IF IT'S THE TARGET
            # if v == destination_vertex:
            # print("master plan", master_plan)
            # print("What's in this room's map", master_plan[v.id].values())
            if '?' in master_plan[v.id].values():
                # IF SO, RETURN PATH
                return path
            # Mark it as visited...
            visited.add(v.id)
            # Then add A PATH TO its neighbors to the back of the queue
                # COPY THE PATH
                # APPEND THE NEIGHOR TO THE BACK
            for next_room in v.get_exits():
                
                # print(f'room {v.id} should altogether show {v.get_exits()}. this time is {next_room}')
                new_path = path.copy() 
                # print("Next room", next_room)
                # print("v.getroomindirection", v.get_room_in_direction(next_room))
                new_path.append(v.get_room_in_direction(next_room))
                # print(f"New Path last id is {new_path[-1].id}")
                # print([i.id for i in new_path])  # why is this returning a None type. 
                q.enqueue(new_path)
    print("Close to returning None")
    return None # WHy is this getting hit? It should be avoided. There should be a vertex added to stack and it should be 

# CONCLUSION--- THIS FUNCTION'S QUEUE SIZE IS SHRUNK TO ZERO BEFORE IT SHOULD BE AT ZERO

print("Current Room 194", current_room)
path = bfs(current_room)
print("Path", path)
intpath = [p.id for p in path]
print(intpath)

# travel to intpath[-1]
print("Current room", current_room.id)
print(intpath[-1])



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
