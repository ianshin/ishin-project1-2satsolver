import os 
import time
import matplotlib
import matplotlib.pyplot as plt
from cnf_parser import parse_cnf
from implication_graph import build_implication_graph
from scc import kosaraju_scc, is_satisfiable 

# Test files location
TEST_FILES_DIR = "test_files/"


# Solving a single 2-SAT problem. 
# Parameter: wff
# Returns a tuple. 

def solve_2sat(wff):
    print("Solving 2-SAT problem...")

    start_time = time.time()

    try:
        # 1. Build implication graph
        implication_graph = build_implication_graph(wff['clauses'], wff['num_variables'])
        
        # Print the implication graph
        print("\n--- Implication Graph ---")
        for node, neighbors in implication_graph.items():
            print(f"{node}: {neighbors}")
        print("-------------------------\n")

        # 2. Find Strongly Connected Components (SCCs) 
        sccs = kosaraju_scc(implication_graph, wff['num_variables'])
        
        # Print the SCCs
        print("\n--- Strongly Connected Components (SCCs) ---")
        for scc in sccs:
            print(f"SCC: {scc}")
        print("---------------------------------------------\n")     

        # 3. Check satisfiability
        satisfiable = is_satisfiable(sccs)

    except Exception as e:
        print(f"An error occurred while solving: {e}")
        return None, None, None, None 

    end_time = time.time()
    execution_time = end_time - start_time

    return satisfiable, execution_time, implication_graph, sccs


# Run the 2-SAT solver on both CNF test files in the test_files/ directory

def run_tests():
    test_files = [ 
        "test_10vars.cnf.csv",
        "test_50vars.cnf.csv",
        "test_100vars.cnf.csv",
        "test_200vars.cnf.csv",
        "test_500vars.cnf.csv"
    ]

    results = []

    # Open a file to store output
    with open("results.txt", "w") as output_file, open("detailed_output.txt", "w") as detailed_file:

        for file_name in test_files:
            cnf_file_path = os.path.join(TEST_FILES_DIR, file_name)
            
            if os.path.exists(cnf_file_path):
                output_file.write(f"Processing file: {cnf_file_path}\n")
                detailed_file.write(f"Processing file: {cnf_file_path}\n")
                print(f"Processing file: {cnf_file_path}")
                
                try:
                    # 1. Parse the CNF file 
                    wff = parse_cnf(cnf_file_path)
                    
                    # Success message in results.txt 
                    output_file.write(f"File {file_name} parsed successfully.\n")
                    
                    # Adding parsed CNF details to output files
                    detailed_file.write(f"\n--- Parsed CNF File: {file_name} ---\n")
                    detailed_file.write(f"Number of Variables: {wff['num_variables']}\n")
                    detailed_file.write(f"Number of Clauses: {wff['num_clauses']}\n")
                    detailed_file.write(f"Clauses: {wff['clauses']}\n")

                    # 2. Solve the 2-SAT problem 
                    satisfiable, exec_time, implication_graph, sccs = solve_2sat(wff)

                    if satisfiable is None:
                        output_file.write(f"An error occurred while processing {file_name}\n")
                        detailed_file.write(f"An error occurred while processing {file_name}\n")
                        print(f"An error occurred while processing {file_name}")
                        continue

                    # Collect results for plotting
                    results.append((wff['num_variables'], exec_time))

                    # Results output
                    output_file.write(f"\n--- Result for {file_name} ---\n")
                    output_file.write(f"Satisfiable: {'Yes' if satisfiable else 'No'}\n")
                    output_file.write(f"Execution Time: {exec_time:.6f} seconds\n")
                    output_file.write("\n" + "-"*40 + "\n") 

                    # Write implication graph and SCCs to detailed_output.txt
                    detailed_file.write(f"\n--- Implication Graph for {file_name} ---\n")
                    for node, neighbors in implication_graph.items():
                        detailed_file.write(f"{node}: {neighbors}\n")

                    detailed_file.write(f"\n--- Strongly Connected Components (SCCs) for {file_name} ---\n")
                    for scc in sccs:
                        detailed_file.write(f"SCC: {scc}\n")
                    detailed_file.write("\n" + "-"*40 + "\n")

                except Exception as e:
                    output_file.write(f"Error processing {file_name}: {e}\n")
                    detailed_file.write(f"Error processing {file_name}: {e}\n")
                    print(f"Error processing {file_name}: {e}")
            else:
                output_file.write(f"File not found: {file_name}\n")
                detailed_file.write(f"File not found: {file_name}\n")
                print(f"File not found: {file_name}")

    # Generate performance plot
    if results:
        plot_performance(results)

# Plot axes: Execution time vs number of variables 
def plot_performance(results):
    variables = [x[0] for x in results]
    times = [x[1] for x in results]

    plt.plot(variables, times, marker='o')
    plt.title("Execution Time vs Number of Variables")
    plt.xlabel("Number of Variables")
    plt.ylabel("Execution Time (sec)")
    plt.grid(True)

    print("Saving performance plot as 'performance_plot.png'")
    plt.savefig("performance_plot.png")
    plt.show()

if __name__ == "__main__":
    run_tests()

