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

def compute_path_to_terminal(starting_vertex, map, master_plan, terminal):
    # print("Current Room", current_room)
    traversal_path = []
    current_room = starting_vertex.id
    directions_by_room = map[terminal]
    directions_by_compass = []
    print(f"Directions by room to {terminal}", directions_by_room)
    for next_room in directions_by_room[1:]: # ex 7 8 
        for direction in master_plan[current_room]: # for n/s/e/w in {... 0: {'n': 1, 's': 5, 'w': 7, 'e': 3} ...}
            print("current room", current_room,'next room', next_room,  "master plan[curent room]", master_plan[current_room], "Direction", direction)
            if master_plan[current_room][direction] == next_room: # if master_plan[0]['w'] == 7
                directions_by_compass.append(direction) # [].append('w')
                current_room = next_room
                break

    print("directions by compass", directions_by_compass, "to room ", terminal)
    return traversal_path

def compute_path_to_terminals(starting_vertex, map, master_plan, terminal_list):
    # print("Current Room", current_room)
    traversal_path = []
    for terminal in terminal_list:
        current_room = starting_vertex.id
        directions_by_room = map[terminal]
        directions_by_compass = []
        directions_back = []
        print(f"Directions by room to {terminal}", directions_by_room)
        for next_room in directions_by_room[1:]: # ex 7 8 
            for direction in master_plan[current_room]: # for n/s/e/w in {... 0: {'n': 1, 's': 5, 'w': 7, 'e': 3} ...}
                if master_plan[current_room][direction] == next_room: # if master_plan[0]['w'] == 7
                    directions_by_compass.append(direction) # [].append('w')
                    current_room = next_room
                    break
            print("Directions by compass" , directions_by_compass)
            for _ in reversed(directions_by_compass):
                print("i am reversed", _)

        print("directions by compass", directions_by_compass, "to room ", terminal)
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
                    terminals.add(v_obj.id)
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

            # This needs to be conditional. Need to avoid terminating and looping paths. Need a check or flag to identify and need a way to scope that identification and scope and stackframe the data so it is at the right level for us when we need it. Challenging to be conscious of this. Lack of conscoiusness of this though it's challenging is where the rub is.
            #  
            next_room = v_obj.get_room_in_direction(direction) # This is 'moving'
            
            master_plan[v_obj.id][direction] = next_room.id
            if next_room.id not in master_plan:
                master_plan[next_room.id] = {}
                for exit in next_room.get_exits():
                    master_plan[next_room.id][exit] = '?'
            
            master_plan[next_room.id][translate(direction)] = v_obj.id
            # print("master plan coming together", master_plan)
            print('v_obj', v_obj)



            q.append(next_room) # This needs to be conditional. It will cause endless recursion. 
            traversal_path.append(direction) # So we added the direction we moved to the path but we are moving too much for no good reason. 

    print("final rooms visited", visited)
    return traversal_path

tuple_return = bfts(world.starting_room)
room_map = tuple_return[1]
master_plan = tuple_return[2]
terminal_list= list(tuple_return[3])
print("Traversal Path (Incorrect):", tuple_return[0])
print("Visited:", tuple_return[1])
print("Master Plan:", tuple_return[2])
print("Terminal List:", tuple_return[3])

# for terminal in terminal_list:
#     compute_path_to_terminals(world.starting_room,room_map, master_plan, terminal)
compute_path_to_terminals(world.starting_room,room_map, master_plan, terminal_list)

traversal_path = tuple_return[0]
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
