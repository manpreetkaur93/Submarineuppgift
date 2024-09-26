import os
from logger import movement_logger, log_collision

class Submarine:
    """Representerar en ubåt med möjlighet att röra sig och kontrollera kollisioner."""
    def __init__(self, serial_number):
        """Initierar en ny ubåt."""
        self.serial_number = serial_number
        self.position = [0, 0]  # [djupt, horizontel]
        self.movement_log = []
        self.positions = {}  # Dictionary för att lagra positioner med tidsindex
        self.time_index = 0  # Tidsindex
        self.positions[self.time_index] = tuple(self.position)

    @movement_logger
    def move_up(self, value):
        """Flyttar ubåten uppåt."""
        self.position[0] -= value  # Minska djupet när båten rör sig uppåt
        self.log_movement(f"up {value}")

    @movement_logger
    def move_down(self, value):
        """Flyttar ubåten nedåt. """
        self.position[0] += value  # Öka djupet när båten rör sig nedåt
        self.log_movement(f"down {value}")

    @movement_logger
    def move_forward(self, value):
        """Flyttar ubåten framåt."""
        self.position[1] += value  # Flytta horisontellt framåt
        self.log_movement(f"forward {value}")

    def log_movement(self, movement):
        """Loggar en rörelse och uppdaterar position och tidsindex. """
        self.movement_log.append(movement)
        self.time_index += 1  # Öka tidsindex
        self.positions[self.time_index] = tuple(self.position)

    def check_collision(self, other_submarine):
        """Kontrollerar om det finns någon kollision med en annan ubåt."""
        collision_positions = []
        common_times = set(self.positions.keys()).intersection(other_submarine.positions.keys())
        for time in common_times:
            if self.positions[time] == other_submarine.positions[time]:
                collision_positions.append((self.positions[time], time))
                # Logga kollisionen
                log_collision(self, other_submarine, self.positions[time], time)
                print(f"Kollision upptäckt mellan {self.serial_number} och {other_submarine.serial_number} på position {self.positions[time]} vid tid {time}")
        return collision_positions

    def load_movements(self, filepath):
        """ Laddar in rörelser från en fil."""
        if not os.path.exists(filepath):
            print(f"Rörelsefil hittades inte för ubåt {self.serial_number}")
            # Logga felet
            log_error(f"Movement file not found for submarine {self.serial_number}")
            return
        try:
            direction_methods = {
                'up': self.move_up,
                'down': self.move_down,
                'forward': self.move_forward
            }
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
                    if direction in direction_methods:
                        direction_methods[direction](value)
                    else:
                        print(f"Ogitlig riktning i rörelsefilen för {self.serial_number} på rad {line_number}: {line.strip()}")
        except Exception as e:
            print(f"Fel vid inläsning av rörelser för {self.serial_number}: {e}")
            # Logga felet
            from logger import log_error
            log_error(f"Error loading movements for {self.serial_number}: {e}")

    def distance_from_start(self):
        """Beräknar avståndet från startpositionen till nuvarande position."""
        depth = self.position[0]
        horizontal = self.position[1]
        return (depth**2 + horizontal**2) ** 0.5

    def can_fire_torpedo(self, direction, submarines):
        """ Kontrollerar om ubåten kan avfyra en torped i en given riktning utan risk för friendly fire."""
        target_position = self.get_target_position(direction)
        for sub in submarines.values():
            if sub.serial_number != self.serial_number and tuple(sub.position) == tuple(target_position):
                return False
        return True

    def get_target_position(self, direction):
        """ Beräknar målpositionen baserat på riktning."""
        if direction == 'forward':
            return [self.position[0], self.position[1] + 1]
        elif direction == 'up':
            return [self.position[0] - 1, self.position[1]]
        elif direction == 'down':
            return [self.position[0] + 1, self.position[1]]
        else:
            return self.position
