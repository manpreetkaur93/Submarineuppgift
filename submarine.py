import os
from logger import movement_logger, log_collision

class Submarine:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.position = [0, 0]  # [depth, horizontal]
        self.movement_log = []
        self.positions = {}  # Ändra till ordbok för att lagra positioner med tidsindex
        self.time_index = 0  # Introducera tidsindex
        self.positions[self.time_index] = tuple(self.position)

    @movement_logger
    def move_up(self, value):
        self.position[0] -= value  # Minska djupet när vi rör oss uppåt
        self.log_movement(f"up {value}")

    @movement_logger
    def move_down(self, value):
        self.position[0] += value  # Öka djupet när vi rör oss nedåt
        self.log_movement(f"down {value}")

    @movement_logger
    def move_forward(self, value):
        self.position[1] += value  # Flytta horisontellt framåt
        self.log_movement(f"forward {value}")

    def log_movement(self, movement):
        self.movement_log.append(movement)
        self.time_index += 1  # Öka tidsindex
        self.positions[self.time_index] = tuple(self.position)

    def check_collision(self, other_submarine):
     collision_positions = []
     common_times = set(self.positions.keys()).intersection(other_submarine.positions.keys())
     for time in common_times:
        pos1 = self.positions[time]
        pos2 = other_submarine.positions[time]
        if pos1 == pos2:
            collision_positions.append((pos1, time))
     if collision_positions:
        for pos, time in collision_positions:
            log_collision(self, other_submarine, pos, time)
            print(f"Kollision upptäckt mellan {self.serial_number} och {other_submarine.serial_number} på position {pos} vid tid {time}")
     return collision_positions  

    def load_movements(self, filepath):
        if not os.path.exists(filepath):
            print(f"Rörelsefil hittades inte för ubåt {self.serial_number}")
            # Logga felet
            from logger import log_error
            log_error(f"Movement file not found for submarine {self.serial_number}")
            return
        try:
            with open(filepath, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    parts = line.strip().split()
                    if len(parts) != 2:
                        print(f"Ogiltilig rad i rörelsefilen för {self.serial_number} på rad {line_number}: {line.strip()}")
                        continue  # Hoppar över ogiltiga rader
                    direction, value = parts
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Ogitligt värde i rörelsefilen för {self.serial_number} på rad {line_number}: {line.strip()}")
                        continue  # Hoppar över rader med ogiltiga tal
                    if direction == 'up':
                        self.move_up(value)
                    elif direction == 'down':
                        self.move_down(value)
                    elif direction == 'forward':
                        self.move_forward(value)
                    else:
                        print(f"Ogitlig riktning i rörelsefilen för {self.serial_number} på rad {line_number}: {line.strip()}")
        except Exception as e:
            print(f"Fel vid inläsning av rörelser för {self.serial_number}: {e}")
            # Logga felet
            from logger import log_error
            log_error(f"Error loading movements for {self.serial_number}: {e}")

    def distance_from_start(self):
        depth = self.position[0]
        horizontal = self.position[1]
        return (depth**2 + horizontal**2) ** 0.5

    def can_fire_torpedo(self, direction, submarines):
        target_position = self.get_target_position(direction)
        for sub in submarines.values():
            if sub.serial_number != self.serial_number and tuple(sub.position) == tuple(target_position):
                # Risk för friendly fire
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
