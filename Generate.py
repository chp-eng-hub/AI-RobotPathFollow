#!/usr/bin/env python3

import csv
import random

def create_random_coordinates(num_points, output_file, width, height):
    # Generate random coordinates
    points = [(random.uniform(0,width), random.uniform(0,height)) for _ in range(num_points - 1)]

    # Add (0, 0) as the first coordinate
    points.insert(0, (0.0, 0.0))

    # Write to CSV
    with open(output_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        # Add header
        csv_writer.writerow(["X (mm)", "Y (mm)"])
        for point in points:
            csv_writer.writerow(point)
    print(f"{num_points} random coordinates written to {output_file}.")

def main():
    num_points = 100  # Number of points to generate
    output_file = 'pointset.csv'
    width = 800
    height = 800
    create_random_coordinates(num_points, output_file, width, height)

if __name__ == '__main__':
    main()