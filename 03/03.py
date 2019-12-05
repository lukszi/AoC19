import numpy as np
from numpy import int8, int32, int16
from matplotlib import pyplot as plt
import json


def calculate_dimensions(wire):
    min_coords = [0, 0]
    max_coords = [0, 0]
    curr = [0, 0]
    commands = wire.split(",")
    for command in commands:
        # Parse command
        direction = command[0]
        length = int(command[1:])

        # Simulate command
        if direction == "U":
            curr[1] = curr[1] + length
        elif direction == "D":
            curr[1] = curr[1] - length
        elif direction == "R":
            curr[0] = curr[0] + length
        elif direction == "L":
            curr[0] = curr[0] - length

        # Update min and max
        min_coords = [min(min_coords[0], curr[0]), min(min_coords[1], curr[1])]
        max_coords = [max(max_coords[0], curr[0]), max(max_coords[1], curr[1])]
    return min_coords, max_coords


class WireMatrix:
    wires = None
    grid = None
    pos = None
    central_port_pos = None
    offset = None
    distances = {}
    steps_so_far = 1

    def __init__(self, wire1, wire2):
        self.wires = [wire1, wire2]
        self.__init_grid()
        self.__paint_wires()

    #
    # Paints all wires in the wires list
    #
    def __paint_wires(self):
        for i in range(0, len(self.wires)):
            # Reset draw position
            self.__reset_pos()
            wire = self.wires[i]
            # Split Commands
            commands = wire.split(",")
            # print("Painting wire " + str(i))
            for command in commands:
                self.__do_command(command, pow(2, i+1))

    #
    # Executes a single command like U30
    #
    def __do_command(self, command, encoding):
        # print("Executing: " + command)
        direction = command[0]
        length = int(command[1:])
        for i in range(0, length):
            self.__do_atomic_command(direction, encoding)
        # print("Pos now at: " + str(self.pos))
        # print("np  now at: " + str(self.trans_np(self.pos)))

    #
    # Resets Position to the base and the steps to 0
    #
    def __reset_pos(self):
        self.pos = [0, 0]
        self.steps_so_far = 1

    #
    # Performs an atomic command into one direction
    #
    def __do_atomic_command(self, direction, encoding):
        if direction == "U":
            self.pos[1] = self.pos[1] + 1
            self.print_wire_position(encoding)
        elif direction == "D":
            self.pos[1] = self.pos[1] - 1
            self.print_wire_position(encoding)
        elif direction == "R":
            self.pos[0] = self.pos[0] + 1
            self.print_wire_position(encoding)
        elif direction == "L":
            self.pos[0] = self.pos[0] - 1
            self.print_wire_position(encoding)
        self.steps_so_far = self.steps_so_far+1

    def trans_np(self, cartesian_coordinates, level=0):
        return cartesian_coordinates[0] + self.offset[0], cartesian_coordinates[1] + self.offset[1],

    def trans_cart(self, cartesian_coordinates):
        return [cartesian_coordinates[0] - self.offset[0], cartesian_coordinates[1] - self.offset[1]]

    #
    # Finds all cross sections for a list of encodings
    #
    def find_all_cross_sections(self, encodings):
        result = np.where(self.grid == 6)
        return list(zip(result[0], result[1]))

    def __init_grid(self):
        # Calculate minimum and maximum reachable coords assuming a [0,0] based coordinate system for each wire
        (min_coords1, max_coords1) = calculate_dimensions(self.wires[0])
        (min_coords2, max_coords2) = calculate_dimensions(self.wires[1])

        # Calculate min and max globally
        min_coords = [min(min_coords1[0], min_coords2[0]), min(min_coords1[1], min_coords2[1])]
        max_coords = [max(max_coords1[0], max_coords2[0]), max(max_coords1[1], max_coords2[1])]

        # Calculate Size of the array such that no access into negative areas happens
        size = (abs(min_coords[0])+abs(max_coords[0])+1, abs(min_coords[1])+abs(max_coords[1])+1)

        # Create Array
        self.grid = np.zeros(size, dtype=int8)

        # Calculate offset to [0, 0] for the newly created array
        self.offset = (-min_coords[0], -min_coords[1])

        # Calculate position for the central pos
        self.central_port_pos = [0, 0]
        self.grid[self.trans_np([0, 0])] = 1
        # print("central_port_pos", self.central_port_pos)
        pass

    #
    # Adds a wire at the current position
    #
    def print_wire_position(self, encoding):
        value = self.grid[self.trans_np(self.pos)]
        # Check if there already is a wire, if so return
        if (value & encoding) == encoding:
            return
        else:
            self.grid[self.trans_np(self.pos)] = value + encoding
            # self.grid[self.trans_np(self.pos, encoding)] = self.steps_so_far
        self.distances[self.trans_np(self.pos), encoding] = self.steps_so_far


if __name__ == "__main__":
    with open("wires.json", "r") as wiresFile:
        wires = json.load(wiresFile)
    wire_a = wires[0]["wire_a"]
    wire_b = wires[0]["wire_b"]
    matrix = WireMatrix(wire_a, wire_b)
    # print("created")
    cross_sections = matrix.find_all_cross_sections([2, 4])
    min_dist = abs(cross_sections[0][0]) + abs(cross_sections[0][1])
    for candidate in cross_sections:
        candidate = matrix.trans_cart(candidate)
        dist = abs(candidate[0]) + abs(candidate[1])
        if dist < min_dist:
            min_dist = dist
    print("shortest distance is: " + str(min_dist))
    # plt.imsave("img.png", matrix.grid)
    dist_wire_1 = matrix.distances[((cross_sections[0][0], cross_sections[0][1]), 2)]
    dist_wire_2 = matrix.distances[((cross_sections[0][0], cross_sections[0][1]), 4)]
    min_dist = dist_wire_1 + dist_wire_2

    for candidate_np in cross_sections:
        candidate = matrix.trans_cart(candidate_np)
        dist_wire_1 = matrix.distances[((candidate_np[0], candidate_np[1]), 2)]
        dist_wire_2 = matrix.distances[((candidate_np[0], candidate_np[1]), 4)]
        dist = dist_wire_1 + dist_wire_2
        # print("Candidate " + str(candidate) + " has dist " + str(dist))
        if dist < min_dist:
            min_dist = dist
    print("MinDist is: " + str(min_dist))
