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

def reverse_direction(array):
    new_array = []
    for item in array:
        new_array.append(translate(item))
    return new_array

def print_q_ids(q):
    q_ids = []
    for obj in q:
        q_ids.append(obj.id)
    print("queue ids", q_ids)

# Load world
world = World()

rooms_visited = set()
# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

def add_to_visited(room_id):
    rooms_visited.add(room_id)

def compute_path_to_terminal(starting_vertex, map, master_plan, terminal):
    # print("Current Room", current_room)
    traversal_path = []
    current_room = starting_vertex
    directions_by_room = map[terminal]
    directions_by_compass = []
    add_to_visited(current_room)
    # print(f"Directions by room to {terminal}", directions_by_room)
    for next_room in directions_by_room[1:]: # ex 7 8
        add_to_visited(next_room) 
        for direction in master_plan[current_room]: # for n/s/e/w in {... 0: {'n': 1, 's': 5, 'w': 7, 'e': 3} ...}
            # print("current room", current_room,'next room', next_room,  "master plan[curent room]", master_plan[current_room], "Direction", direction)
            if master_plan[current_room][direction] == next_room: # if master_plan[0]['w'] == 7
                directions_by_compass.append(direction) # [].append('w')
                current_room = next_room
                break
    # ruckwarts = reverse_direction(reversed(directions_by_compass))
    # print(f"directions by compass to {terminal}", directions_by_compass)
    traversal_path = directions_by_compass
    # print("Traversal path bit", traversal_path)
    traversal_path.extend(reverse_direction(reversed(directions_by_compass)))
    # print("directions by compass", directions_by_compass, "to room ", terminal)    
    return traversal_path



def bfts(starting_vertex):   # Breadth first traversal-search

    visited = {} 
    # !!!! IMPLEMENT ME
    q = Queue()
    traversal_path = []
    q.enqueue([starting_vertex])
    master_plan[starting_vertex.id] = {}
    for exit in starting_vertex.get_exits():
        master_plan[starting_vertex.id][exit] = '?'
    print("master plan:", master_plan)
    terminals = set()

    while q.size() > 0:
        path = q.dequeue()
        v_obj = path[-1]
        if v_obj.id not in master_plan:
            master_plan[v_obj.id] = {}
            for exit in v_obj.get_exits():
                master_plan[v_obj.id][exit] = '?'
        
        if v_obj.id not in visited:
            path_ids = []
            returning = False
            for _ in path:
                path_ids.append(_.id)
            visited[v_obj.id] = path_ids
            for direction in v_obj.get_exits():
                if len(v_obj.get_exits()) == 1: # Base case of terminus
                    terminals.add(v_obj.id) # Rooms that are end of the line

                # Need an algorithm for identifying loops and wlaking them once
                path_copy = list(path)
                next_room = v_obj.get_room_in_direction(direction)
                traversal_path.append(direction)
                path_copy.append(next_room)
                q.enqueue(path_copy)

                master_plan[v_obj.id][direction] = next_room.id
                if next_room.id not in master_plan:
                    master_plan[next_room.id] = {}
                    for exit in next_room.get_exits():
                        master_plan[next_room.id][exit] = '?'
                
                master_plan[next_room.id][translate(direction)] = v_obj.id
                # print("master plan coming together", master_plan)

    # print("Visited",visited)
    tuple_return = (traversal_path, visited, master_plan, terminals)
    print("Terminal Rooms", terminals)
    return tuple_return


tuple_return = bfts(world.starting_room)
room_map = tuple_return[1]
master_plan = tuple_return[2]
terminal_list= list(tuple_return[3])
# print("Traversal Path (Incorrect):", tuple_return[0])
# print("Visited:", tuple_return[1])
# print("Master Plan:", tuple_return[2])
# print("Terminal List:", tuple_return[3])
traversal_path = []
for terminal in terminal_list:
    traversal_path.extend(compute_path_to_terminal(world.starting_room.id,room_map, master_plan, terminal))
    
# compute_path_to_terminals(world.starting_room,room_map, master_plan, terminal_list)
# print("final traversal path", traversal_path)
# print("Rooms visited", rooms_visited)
while len(master_plan) > len(rooms_visited):
    unvisited_rooms = set()
    for _ in range(len(master_plan)):
        if _ not in rooms_visited:
            unvisited_rooms.add(_)
    rand_ = random.randint(0, len(unvisited_rooms)-1)
    pseudo_terminal = list(unvisited_rooms)[rand_]
    # print("pseudo terminal", pseudo_terminal)
    # print("unvisited rooms", unvisited_rooms)
    traversal_path_extension = compute_path_to_terminal(world.starting_room.id, room_map, master_plan, pseudo_terminal)
    # print('traversal path extension', traversal_path_extension)
    traversal_path.extend(traversal_path_extension)

grid = [0,0]
set_of_indices = []
for index, unit in enumerate(traversal_path):
    # print('index, unit', index, unit)
    if unit == 'e':
        grid[0] += 1
    elif unit == 'w':
        grid[0] -= 1
    elif unit == 'n':
        grid[1] += 1
    elif unit == 's':
        grid[1] -= 1
    if grid == [0,0]:
        set_of_indices.append(index+1)
# print('set of indices', set_of_indices, len(set_of_indices))
prior_index = 0
path_of_paths = []
for i,index in enumerate(set_of_indices):
    # print("i", i, "index", index)
    # print('traversal path[prior_index:index', traversal_path[prior_index:index])
    path_of_paths.append(traversal_path[prior_index:index])
    prior_index = index

# Got a list of lists made of all the paths that go from origin to origin. THat is huge. Now I have to see if the first half of each one is redundant- a subset of another path. 
# print("Path of paths before halved path", path_of_paths)
halved_path_of_paths = []
# print("Path of paths before halved path", path_of_paths)

for index, path in enumerate(path_of_paths):
    halved_path_of_paths.append(path[:int(len(path)/2)])
    print("Path of paths", path)
    print("halved version", halved_path_of_paths[index])





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