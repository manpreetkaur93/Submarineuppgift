import os
from logger import movement_logger, log_collision

class Submarine:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.position = [0, 0]  # [depth, horizontal]
        self.movement_log = []
        self.positions = set()
        self.positions.add(tuple(self.position))

    @movement_logger
    def move_up(self, value):
        self.position[0] -= value  # Decrease depth when moving up
        self.log_movement(f"up {value}")

    @movement_logger
    def move_down(self, value):
        self.position[0] += value  # Increase depth when moving down
        self.log_movement(f"down {value}")

    @movement_logger
    def move_forward(self, value):
        self.position[1] += value
        self.log_movement(f"forward {value}")

    def log_movement(self, movement):
        self.movement_log.append(movement)
        self.positions.add(tuple(self.position))

    def check_collision(self, other_submarine):
        if tuple(self.position) == tuple(other_submarine.position):
            log_collision(self, other_submarine)
            print(f"Kollision upptäckt mellan {self.serial_number} och {other_submarine.serial_number}")

    def load_movements(self, filepath):
        if not os.path.exists(filepath):
            print(f"Movement file not found for submarine {self.serial_number}")
            return
        try:
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
        except Exception as e:
            print(f"Error loading movements for {self.serial_number}: {e}")

    def distance_from_start(self):
        depth = self.position[0]
        horizontal = self.position[1]
        return (depth**2 + horizontal**2) ** 0.5

    def can_fire_torpedo(self, direction, submarines):
        target_position = self.get_target_position(direction)
        for sub in submarines.values():
            if sub.serial_number != self.serial_number and tuple(sub.position) == tuple(target_position):
                # Risk of friendly fire
                return False
        return True

    def get_target_position(self, direction):
        if direction == 'forward':
            return [self.position[0], self.position[1] + 1]
        elif direction == 'up':
            return [self.position[0] - 1, self.position[1]]
        elif direction == 'down':
            return [self.position[0] + 1, self.position[1]]
        else:
            return self.position
