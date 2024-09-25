import os
from logger import log_error

class SensorData:
    """Hanterar inläsning och analys av sensordata för en ubåt."""

    def __init__(self, sensor_file):
        """Initierar SensorData-objektet"""
        self.sensor_file = sensor_file
        self.sensor_failures = []
        self.error_count = {}
        self.total_sensors = 208  

    def load_sensor_data(self):
        """Laddar in sensordata från filen."""
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
        """antal fel i sensordata."""
        for failure in self.sensor_failures:
            error_positions = tuple(i+1 for i, val in enumerate(failure) if val == '0')  # Sensornummer från 1 till 208
            if error_positions:
                self.error_count[error_positions] = self.error_count.get(error_positions, 0) + 1

    def display_repeated_errors(self):
        """Visar sensorer som har upprepade fel."""
        # Sortera error_count baserat på antal fel i fallande ordning
        sorted_errors = sorted(self.error_count.items(), key=lambda item: item[1], reverse=True)
        for error_positions, count in sorted_errors:
            if count > 1:
                sensors = ', '.join([f"sensor {pos} av {self.total_sensors}" for pos in error_positions])
                print(f"Fel på {sensors} inträffade {count} gånger")
                # Loggar upprepade fel
                log_error(f"Repeated errors at positions {error_positions} occurred {count} times")

    def log_errors(self):
        """Loggar det totala antalet fel som upptäckts."""
        total_errors = sum(1 for failure in self.sensor_failures if '0' in failure)
        print(f"Totalt antal rader med fel: {total_errors}")
        # Loggar totala antalet fel
        log_error(f"Submarine {self.sensor_file} had total {total_errors} lines with errors")
