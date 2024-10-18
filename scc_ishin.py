# This file contains the logic for finding SCC's utilizing Kosaraju's Algorithm.
# It also includes the 2-SAT satisfiability check. 

from collections import defaultdict

# DFS to process nodes for SCC detection 
# Parameters: graph, node, visited, stack

def dfs(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, stack)
    stack.append(node)


# Reverses the directions of all edges in the graph. 
# Parameters: graph
# Returns a new graph with all edges reversed. 

def reverse_graph(graph):
    reversed_graph = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)
    return reversed_graph


# Finds all SCCs in implication graph using Kosaraju's algorithm.
# Parameters: graph, num_variables 
# Returns a list of SCCs -- each SCC is represented as a list of nodes. 

def kosaraju_scc(graph, num_variables): 
    visited = set()
    stack = []

    # 1. Use DFS and fill stack with nodes in order of completion time 
    for node in range(-num_variables, num_variables + 1): 
        if node == 0:
            continue
        if node not in visited:
            dfs(graph, node, visited, stack)

    # 2. Reverse the graph
    reversed_graph = reverse_graph(graph)

    # 3. Use DFS on the reversed graph in the order of the stack
    visited.clear()
    sccs = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc = []
            dfs(reversed_graph, node, visited, scc)
            sccs.append(scc)

    return sccs


# Determine if the 2-SAT problem is satisfiable based on SCCs
# Parameters: sccs
# Returns true if satisfiable, false if not. 

def is_satisfiable(sccs):
    for scc in sccs:
        for node in scc:
            if -node in scc:
                return False 
    return True 
