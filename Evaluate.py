#!/usr/bin/env python3

import csv
import math

def read_csv(filepath):
    """
    Read coordinates from a CSV file.
    
    :param filepath: Path to the CSV file.
    :return: List of tuples representing coordinates.
    """
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        points = [(float(row["X (mm)"]), float(row["Y (mm)"])) for row in reader]
    return points

def calculate_total_distance(points):
    """
    Calculate the total distance of the path.
    
    :param points: List of (x, y) coordinates.
    :return: Total distance of the path.
    """
    total_distance = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]  # Loop back to the start
        total_distance += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return total_distance

def main():
    # Example: Replace with your CSV file path
    filepath = "pointset_optimized_aco.csv"
    points = read_csv(filepath)
    total_distance = calculate_total_distance(points)
    print(f"Total distance for the path in '{filepath}': {total_distance:.2f} mm")

if __name__ == "__main__":
    main()

