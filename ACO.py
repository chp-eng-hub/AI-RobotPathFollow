#!/usr/bin/env python3

import csv
from aco import AntColony

# Read points from CSV and prepare the node list
def read_from_csv(input_csv_path):
    with open(input_csv_path, "r") as file:
        reader = csv.DictReader(file)
        nodes = [(float(row["X (mm)"]), float(row["Y (mm)"])) for row in reader]
    return nodes

def write_to_csv(output_csv_path, path, nodes):
    """
    Write the optimized path to a CSV file.

    :param output_csv_path: Path to save the optimized CSV.
    :param path: List of indices representing the optimized path.
    :param nodes: List of coordinates (nodes).
    """
    with open(output_csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X (mm)", "Y (mm)"])
        if isinstance(path[0], tuple):  # If path contains coordinate tuples
            writer.writerows(path)
        else:  # If path contains indices
            for index in path:
                writer.writerow(nodes[index])


# Run the Ant Colony Optimization
if __name__ == "__main__":
    input_csv_path = "pointset.csv"
    output_csv_path = "pointset_optimized_aco_test.csv"

    # Read nodes from CSV
    nodes = read_from_csv(input_csv_path)

    # Initialize the Ant Colony
    ant_colony = AntColony(
        nodes=nodes,
        start=0,  # Assuming the first node is the starting point
        ant_count=50,
        alpha=1.0,
        beta=2.0,
        pheromone_evaporation_rate=0.5,
        pheromone_constant=100.0,
        iterations=100
    )

    # Get the optimized path
    optimized_path = ant_colony.get_path()

    # Save the results to CSV
    write_to_csv(output_csv_path, optimized_path, nodes)
    print(f"Optimized path saved to {output_csv_path}")
