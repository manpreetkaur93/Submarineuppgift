import os
from logger import log_error  # Importera log_error för att logga fel

class SensorData:
    def __init__(self, sensor_file):
        self.sensor_file = sensor_file
        self.sensor_failures = []
        self.error_count = {}
        self.repeated_errors = {}

    def load_sensor_data(self):
        try:
            with open(self.sensor_file, 'r') as file:
                for line in file:
                    self.sensor_failures.append(line.strip())
        except Exception as e:
            log_error(f"Fel vid läsning av sensordata för {self.sensor_file}: {e}")

    def count_errors(self):
        for failure in self.sensor_failures:
            error_positions = [i for i, val in enumerate(failure) if val == '0']
            error_key = tuple(error_positions)
            if error_key in self.error_count:
                self.error_count[error_key] += 1
            else:
                self.error_count[error_key] = 1

    def display_repeated_errors(self):
        for error_positions, count in self.error_count.items():
            if count > 1:
                print(f"Fel på positioner {error_positions} inträffade {count} gånger")
                # Logga återkommande fel
                log_error(f"Återkommande fel på positioner {error_positions} inträffade {count} gånger")

    def log_errors(self):
        simultaneous_errors = 0
        for failure in self.sensor_failures:
            error_count = failure.count('0')
            if error_count >= 1:
                simultaneous_errors += 1
        print(f"Totalt antal rader med fel: {simultaneous_errors}")
        # Logga total antal fel
        log_error(f"Ubåt {self.sensor_file} hade totalt {simultaneous_errors} rader med fel")
