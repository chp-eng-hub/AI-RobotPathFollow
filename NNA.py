#!/usr/bin/env python3

import csv
import numpy as np
import os

def nearest_neighbor(points):
    """
    Optimize the path using the Nearest Neighbor Algorithm.
    :param points: List of (x, y) tuples representing coordinates.
    :return: Optimized path as a list of coordinates and total distance.
    """
    unvisited = points[:]
    path = [unvisited.pop(0)]  # Start with the first point
    total_distance = 0
    while unvisited:
        nearest = min(unvisited, key=lambda p: np.linalg.norm(np.array(path[-1]) - np.array(p)))
        total_distance += np.linalg.norm(np.array(path[-1]) - np.array(nearest))
        path.append(nearest)
        unvisited.remove(nearest)
    # Add distance to return to start point
    total_distance += np.linalg.norm(np.array(path[-1]) - np.array(path[0]))
    return path, total_distance

def read_csv(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        points = [(float(row['X (mm)']), float(row['Y (mm)'])) for row in reader]
    return points

def write_csv(filepath, points):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X (mm)', 'Y (mm)'])
        writer.writerows(points)

if __name__ == "__main__":
    input_csv_path = "pointset.csv"
    output_csv_path = "pointset_optimized_nna.csv"
    

    points = read_csv(input_csv_path)
    print(f"Read {len(points)} points from {input_csv_path}.")

    optimized_points, total_distance = nearest_neighbor(points)
    print("Optimization completed.")
    print(f"Total distance: {total_distance:.2f} mm")

    write_csv(output_csv_path, optimized_points)
    print(f"Optimized points saved to {output_csv_path}.")
