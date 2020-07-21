from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval
import timeit

# Load world
world = World()

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
# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
starting_room = world.starting_room
current_room = world.starting_room
player = Player(world.starting_room)
# Fill this out with directions to walk
traversal_path = []
# traversal_path = ['n', 'n']

def draw_master_plan(v, direction=None, new_room=None):
  if v.id not in master_plan:
    master_plan[v.id] = {}
    for exit in v.get_exits():
      master_plan[v.id][exit] = '?'
  if direction is not None and new_room is not None:
    if new_room.id not in master_plan:
      master_plan[new_room.id] = {}
      for exit in new_room.get_exits():
        master_plan[new_room.id][exit] = '?'
    master_plan[v.id][direction] = new_room.id
    master_plan[new_room.id][mirror(direction)] = v.id
  
def random_step(v=world.starting_room):
  if '?' in master_plan[v.id].values():
    for exit in v.get_exits(): # randomzine
      if master_plan[v.id][exit] == '?':
        new_room = v.get_room_in_direction(exit)
        my_visited_rooms.add(new_room)
        draw_master_plan(v, exit, new_room)
        traversal_path.append(exit)
        return new_room

def find_new_frontier(start):
  q = Queue()
  q.enqueue([start])
  visited = set()
  while q.size() > 0:
    path = q.dequeue()
    v = path[-1]
    if v.id not in visited:
      if '?' in master_plan[v.id].values():
        return path
      visited.add(v.id)
      for next_room in v.get_exits():
        new_path = path.copy()
        new_path.append(v.get_room_in_direction(next_room))
        q.enqueue(new_path)
  return False


### Main ###
start_time = timeit.default_timer()
my_visited_rooms = set()
master_plan = {}
draw_master_plan(starting_room)
my_visited_rooms.add(starting_room)

while len(my_visited_rooms) < len(room_graph):
  if '?' in master_plan[current_room.id].values():
    current_room = random_step(current_room) # Take a step in a new direction
  else:
    backgrack_path = find_new_frontier(current_room) # returns [2,1,0] where 2 is currenr and 0 is frontier and array is path
    for path in backgrack_path:
      for exit in current_room.get_exits():
        if master_plan[current_room.id][exit] == path.id:
          traversal_path.append(exit)
          current_room = current_room.get_room_in_direction(exit)
          break

print(f"Program executed in {round(timeit.default_timer() - start_time, 3)} seconds")
### Done ###        

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

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