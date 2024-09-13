import os  # Viktigt: Se till att denna rad finns i filen

class SensorData:
    def __init__(self, sensor_file):
        self.sensor_file = sensor_file
        self.sensor_failures = []
        self.error_count = {}

    def load_sensor_data(self):
        with open(self.sensor_file, 'r') as file:
            for line in file:
                self.sensor_failures.append(line.strip())

    def count_errors(self):
        for failure in self.sensor_failures:
            if failure in self.error_count:
                self.error_count[failure] += 1
            else:
                self.error_count[failure] = 1

    def display_repeated_errors(self):
        for error, count in self.error_count.items():
            if count > 2:
                print(f"ERROR: {error} occurred {count} times")

def process_all_sensors(folder):
    print(f"Processing sensor data in folder: {folder}")
    for filename in os.listdir(folder):  # Användning av os.listdir()
        if filename.endswith(".txt"):
            sensor_data = SensorData(os.path.join(folder, filename))
            sensor_data.load_sensor_data()
            sensor_data.count_errors()
            sensor_data.display_repeated_errors()
