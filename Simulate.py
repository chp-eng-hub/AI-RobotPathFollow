#!/usr/bin/env python3

import time  # Import the time module
import csv  # Import the csv module
from robodk import robolink, robomath  # Import the RoboDK API

def follow_coordinates(csv_file):
    """
    Make the robot follow a series of coordinates from a CSV file,
    while using the robot's current orientation and working relative to a reference frame.

    :param csv_file: Path to the CSV file containing X, Y, Z coordinates.
    """
    # Initialize RoboDK
    RDK = robolink.Robolink()

    # Get the active robot
    robot = RDK.Item('', robolink.ITEM_TYPE_ROBOT)
    if not robot.Valid():
        raise Exception("No robot selected. Please load and select a robot in RoboDK.")

    # Move the robot to the home position
    robot.MoveJ(robot.JointsHome())

    # Get the reference frame (use the frame name here)
    frame = RDK.Item('Frame')  # Replace 'Frame' with the actual reference frame name in RoboDK
    if not frame.Valid():
        raise Exception("Reference frame not found. Please ensure the correct frame is selected.")

    # Check for existing targets and program, and delete them if they exist
    all_items = RDK.ItemList()
    for item in all_items:
        if item.Type() == robolink.ITEM_TYPE_TARGET or item.Name() == "GeneratedPath":
            item.Delete()

    # Load coordinates from the CSV file with error handling
    coordinates = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                clean_row = [float(value.strip().replace('{', '').replace('}', '')) * 1000 for value in row if value.strip()]
                if len(clean_row) == 3:
                    coordinates.append(tuple(clean_row))
                else:
                    print(f"Skipping malformed row: {row}")
            except ValueError as e:
                print(f"Error parsing row {row}: {e}")
    
    if not coordinates:
        raise Exception("No valid coordinates found in the CSV file.")
    
    # Print sample coordinates for debugging
    print("Sample coordinates:", coordinates[:5])  # Print first 5 coordinates

    # Create a new program
    program = RDK.AddProgram("GeneratedPath", robot)
    program.setRounding(1)

    # Iterate through the coordinates and create targets
    for i, (x, y, z) in enumerate(coordinates, start=1):
        # Define the target position and rotation relative to the frame
        target_position = robomath.transl(x, y, z)

        # Create a target
        target_name = f"Target {i}"
        target = RDK.AddTarget(target_name, frame)
        target.setPose(target_position)

        # Add a move instruction to the program
        program.MoveL(target)

    # Simulate the program to estimate execution time
    result = program.Update(check_collisions=robolink.COLLISION_OFF)

    # The result is a tuple:
    # [valid_instructions, program_time, program_distance, valid_ratio, readable_msg]
    valid_instructions, program_time, program_distance, valid_ratio, readable_msg = result

    # Log the simulation results
    print(f"Simulation Results:")
    print(f"  - Valid instructions: {valid_instructions}")
    print(f"  - Estimated program time: {program_time:.2f} seconds")
    print(f"  - Estimated program distance: {program_distance:.2f} mm")
    print(f"  - Valid ratio: {valid_ratio:.2f}")
    print(f"  - Readable message: {readable_msg}")

    # Execute the generated program
    print("Running the GeneratedPath program...")
    program.RunProgram()  # This executes the program in RoboDK
    print("Program execution complete.")


# Usage
if __name__ == "__main__":

    # Measure the total script execution time
    start_time = time.time()

    # Path to the CSV file
    csv_path = "path.csv"

    # Follow the coordinates
    follow_coordinates(csv_path)

    # Log the total execution time
    total_time = time.time() - start_time
    print(f"Total script execution time: {total_time:.2f} seconds")
