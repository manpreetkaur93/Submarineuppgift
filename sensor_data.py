import os
from logger import log_error

class SensorData:
    def __init__(self, sensor_file):
        self.sensor_file = sensor_file
        self.sensor_failures = []
        self.error_count = {}

    def load_sensor_data(self):
        if not os.path.exists(self.sensor_file):
            print(f"Sensordatafil hittades inte: {self.sensor_file}")
            log_error(f"Sensor data file not found: {self.sensor_file}")
            return
        try:
            with open(self.sensor_file, 'r') as file:
                self.sensor_failures = [line.strip() for line in file]
        except Exception as e:
            print(f"Fel vid inläsning av sensordata för {self.sensor_file}: {e}")
            log_error(f"Error reading sensor data for {self.sensor_file}: {e}")

    def count_errors(self):
        for failure in self.sensor_failures:
            error_positions = tuple(i for i, val in enumerate(failure) if val == '0')
            self.error_count[error_positions] = self.error_count.get(error_positions, 0) + 1

    def display_repeated_errors(self):
        for error_positions, count in self.error_count.items():
            if count > 1:
                print(f"Fel på positioner {error_positions} inträffade {count} gånger")
                # Loggar upprepade fel
                log_error(f"Repeated errors at positions {error_positions} occurred {count} times")

    def log_errors(self):
        simultaneous_errors = sum(1 for failure in self.sensor_failures if failure.count('0') >= 1)
        print(f"Totalt antal rader med fel: {simultaneous_errors}")
        # Loggar totala antalet fel
        log_error(f"Submarine {self.sensor_file} had total {simultaneous_errors} lines with errors")
