import csv
import random

# Generate a random 2-SAT problem and write it to CSV file in CNF format.
# Parameters: num_variables (int), num_clauses (int), output_file (str) 

def generate_2sat_problem(num_variables, num_clauses, output_file):
    clauses = []

    # Ensure a satisfiable case by assigning a valid solution to first few clauses 
    # assignment = {i: random.choice([True, False]) for i in range(1, num_variables + 1)}

    for _ in range(num_clauses):
        # Randomly selected two distinct variables (from 1 to num_variables)
        var1 = random.randint(1, num_variables)
        var2 = random.randint(1, num_variables)
        while var2 == var1:
            var2 = random.randint(1, num_variables) # Ensure distinct variables
        
        # Randomly decide if the variables should be negated (50% chance)
        lit1 = var1 if random.random() > 0.5 else -var1
        lit2 = var2 if random.random() > 0.5 else -var2
       
        # Add the clause [lit1, lit2, 0] (0 marks the end of the clause)
        clauses.append([lit1, lit2, 0])

    # Write the clauses to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Comment line 
        writer.writerow(['c', 'generated', '2', '?'])
        # Problem line 
        writer.writerow(['p', 'cnf', f'{num_variables}', f'{num_clauses}'])
        # Clauses 
        for clause in clauses:
            writer.writerow(clause)

    print(f"Generated 2-SAT problem with {num_variables} variables and {num_clauses} clauses.")
    print(f"File saved as: {output_file}")

# Generate 5 different test files with varying sizes
def generate_multiple_tests():
    test_cases = [
        (10, 30, "test_10vars.cnf.csv"),
        (50, 75, "test_50vars.cnf.csv"),
        (100, 150, "test_100vars.cnf.csv"),
        (200, 300, "test_200vars.cnf.csv"),
        (500, 1000, "test_500vars.cnf.csv"),
    ]

    for num_vars, num_clauses, filename in test_cases:
        generate_2sat_problem(num_vars, num_clauses, f"test_files/{filename}")


# Function Call 
if __name__ == "__main__":
    generate_multiple_tests()


