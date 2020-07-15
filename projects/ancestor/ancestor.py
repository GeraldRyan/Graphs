from util import Stack, Queue  # These may come in handy

def earliest_ancestor(ancestors, starting_node):
    graph = {}
    # make graph
    for a in ancestors:
        if a[1] in graph:
            graph[a[1]].add(a[0])
        else:
            graph[a[1]] = set()

            graph[a[1]].add(a[0])
    
    # print("graph", graph)
    # Search through graph to traverse paths


    # Create a stack to traverse through
    stack = []
    # Create a set of visited nodes/vertices
    visited = set()
    #init the stack with the starting node
    stack.append([starting_node])
    print("stack", stack)
    #While length of stack is greater than zero,
    # 
    result = [] 
    while len(stack) > 0:
        # populate the path variable from the last element in the
        path = stack.pop()
        print("path", path)
        v = path[-1]
        if v not in visited:
            visited.add(v)
            
            if v in graph:
                for next_vert in graph[v]:
                    new_path = list(path)
                    new_path.append(next_vert)
                    stack.append(new_path)

            if len(result) < len(path):
                result = path
            elif len(result) == len(path) and result[-1] > v:
                result = path


    print("starting node", starting_node, "stack:", stack)
    if starting_node not in graph: 
        return -1

    print(graph)
    print("Whole path", path)
    print("Path -1=", path[-1])

    return result[-1]


# {3: {1, 2}, 6: {3, 5}, 7: {5}, 5: {4}, 8: {11, 4}, 9: {8}, 1: {10}}
