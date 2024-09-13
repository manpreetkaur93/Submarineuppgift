# submarine.py
import os

class Submarine:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.position = [0, 0]  # [height, horizontal]
        self.movement_log = []

    def move_up(self, value):
        self.position[0] += value
        self.log_movement(f"up {value}")

    def move_down(self, value):
        self.position[0] -= value
        self.log_movement(f"down {value}")

    def move_forward(self, value):
        self.position[1] += value
        self.log_movement(f"forward {value}")

    def log_movement(self, movement):
        self.movement_log.append(movement)
        print(f"{self.serial_number}: {movement}")

    def load_movements(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                direction, value = line.split()
                if direction == 'up':
                    self.move_up(int(value))
                elif direction == 'down':
                    self.move_down(int(value))
                elif direction == 'forward':
                    self.move_forward(int(value))

def load_all_movements(folder):
    submarines = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            serial_number = filename.split('.')[0]
            submarine = Submarine(serial_number)
            submarine.load_movements(os.path.join(folder, filename))
            submarines.append(submarine)
    return submarines
