import os
from logger import log_collision

class Submarine:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.position = [0, 0]  # [height, horizontal]
        self.movement_log = []

    def move_up(self, value):
        self.position[0] -= value  # Decrease depth when moving up
        self.log_movement(f"up {value}")

    def move_down(self, value):
        self.position[0] += value  # Increase depth when moving down
        self.log_movement(f"down {value}")

    def move_forward(self, value):
        self.position[1] += value
        self.log_movement(f"forward {value}")

    def log_movement(self, movement):
        self.movement_log.append(movement)
        # Optionally log to a file or print for debugging
        # print(f"Current position of {self.serial_number}: Height {self.position[0]}, Horizontal {self.position[1]}")

    def check_collision(self, other_submarine):
        if self.position == other_submarine.position:
            log_collision(self, other_submarine)
            print(f"Collision detected between {self.serial_number} and {other_submarine.serial_number}")

    def load_movements(self, filepath):
        if not os.path.exists(filepath):
            print(f"Movement file not found for submarine {self.serial_number}")
            return
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue  # Skip invalid lines
                direction, value = parts
                try:
                    value = int(value)
                except ValueError:
                    continue  # Skip lines with invalid numbers
                if direction == 'up':
                    self.move_up(value)
                elif direction == 'down':
                    self.move_down(value)
                elif direction == 'forward':
                    self.move_forward(value)
