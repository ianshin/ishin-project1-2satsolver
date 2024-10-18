import csv

# Parsing a single CNF file containing one WFF.
# Returns: a dict with the keys - num_variables, num_clauses, clauses (list of clauses where each clause is a list of literals)

def parse_cnf(file_name): 
    print(f"Parsing file: {file_name}")

    clauses = []
    num_variables = 0
    num_clauses = 0

    with open (file_name, mode='r') as file:
        csvFile = csv.reader(file)
        for i, lines in enumerate(csvFile):
            if not lines:
                continue # Skip empty lines
            
            # Check for BOM in first line and remove it
            if i == 0 and lines[0].startswith('\ufeff'):
                lines[0] = lines[0].replace('\ufeff', '')

            if lines[0].startswith('c'):
                continue
            elif lines[0] == 'p':
                # Parse problem line
                num_variables = int(lines[2])
                num_clauses = int(lines[3])
            else:
                # Parse a clause 
                clause = [int(literal) for literal in lines if literal not in ('', '0')]
                clauses.append(clause)
                if len(clauses) == num_clauses:
                    # Stop after reading the specified number of clauses 
                    break
    
    return {'num_variables': num_variables, 'num_clauses': num_clauses, 'clauses': clauses}

