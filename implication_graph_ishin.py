# This file builds the implication graph for a given set of clauses in a 2-SAT problem.
# Each clause in the form (A ∨ B) is transformed into two implications: ¬A → B and ¬B → A. 


from collections import defaultdict


# Return a dictionary representing the graph.

def build_implication_graph(clauses, num_variables):
    graph = defaultdict(list)

    for clause in clauses:
        if len(clause) == 2:
            a, b = clause 
            # Add implications to graph
            graph[-a].append(b)  # If not a, then b
            graph[-b].append(a)  # If not b, then a 

    return graph 

