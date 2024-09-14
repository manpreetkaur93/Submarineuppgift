import os
import time
from submarine import Submarine
from sensor_data import SensorData
from secret_manager import SecretManager
from logger import log_collision
import random  # Importera random för att välja slumpmässiga ubåtar

# Kommenterad kod för nedladdning och uppackning av filer
'''
# Import för nedladdning och uppackning
import gdown
import zipfile

# Google Drive länkar (uppdatera dessa med dina faktiska länkar)
SECRETS_URL = 'https://drive.google.com/uc?export=download&id=15PeR3Rv4FJbvCu8w87-iX2ml59GutgWP'
SENSORDATA_URL = 'https://drive.google.com/uc?export=download&id=1hkyoC2iR_Z6FXcz4nlGzpmwWD1IlU3il'
MOVEMENTREPORTS_URL = 'https://drive.google.com/uc?export=download&id=1potInXCTfjOijqXRo3XNL0_NwhbkhI0C'

# Funktion för att packa upp en zip-fil
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Nedladdningsfunktion för Google Drive
def download_files():
    # Skapa mappar om de inte redan finns
    os.makedirs('Secrets', exist_ok=True)
    os.makedirs('Sensordata', exist_ok=True)
    os.makedirs('MovementReports', exist_ok=True)

    # Ladda ner och packa upp endast om zip-filerna inte redan finns
    if not os.path.exists('Secrets/SecretKEY.txt'):
        print("Downloading Secrets...")
        gdown.download(SECRETS_URL, 'Secrets/secrets.zip', quiet=False)
        time.sleep(2)
        unzip_file('Secrets/secrets.zip', 'Secrets')
    else:
        print("Secrets already downloaded and extracted.")

    if not os.path.exists('Sensordata/sensordata.zip'):
        print("Downloading Sensordata...")
        gdown.download(SENSORDATA_URL, 'Sensordata/sensordata.zip', quiet=False)
        time.sleep(2)
        unzip_file('Sensordata/sensordata.zip', 'Sensordata')
    else:
        print("Sensordata already downloaded and extracted.")

    if not os.path.exists('MovementReports/movementreports.zip'):
        print("Downloading MovementReports...")
        gdown.download(MOVEMENTREPORTS_URL, 'MovementReports/movementreports.zip', quiet=False)
        time.sleep(2)
        unzip_file('MovementReports/movementreports.zip', 'MovementReports')
    else:
        print("MovementReports already downloaded and extracted.")
'''

# Function to list all submarine serial numbers
def list_submarine_serials(folder):
    return [filename.split('.')[0] for filename in os.listdir(folder) if filename.endswith(".txt")]

# Function to allow the user to select a submarine by entering the serial number
def select_submarine(serials):
    while True:
        serial_number = input("Ange serienumret för den ubåt du vill välja: ")
        if serial_number in serials:
            return serial_number
        else:
            print("Ubåten hittades inte. Försök igen.")

# Function to find closest, farthest, highest, and lowest submarines
def find_extreme_submarines(submarines):
    sorted_by_distance = sorted(submarines.values(), key=lambda sub: sub.distance_from_start())
    closest_sub = sorted_by_distance[0]
    farthest_sub = sorted_by_distance[-1]

    sorted_by_depth = sorted(submarines.values(), key=lambda sub: sub.position[0])
    highest_sub = sorted_by_depth[0]
    lowest_sub = sorted_by_depth[-1]

    print(f"Närmaste ubåt: {closest_sub.serial_number}, Avstånd: {closest_sub.distance_from_start()}")
    print(f"Längst bort ubåt: {farthest_sub.serial_number}, Avstånd: {farthest_sub.distance_from_start()}")
    print(f"Högsta ubåt: {highest_sub.serial_number}, Höjd: {highest_sub.position[0]}")
    print(f"Lägsta ubåt: {lowest_sub.serial_number}, Höjd: {lowest_sub.position[0]}")

def main():
    # Ensure necessary directories exist
    os.makedirs('logs', exist_ok=True)

    # List all submarine serial numbers
    print("Lister alla ubåtar...")
    submarine_serials = list_submarine_serials('MovementReports')

    # Initialize the secret manager
    secret_manager = SecretManager('Secrets/Secrets/SecretKEY.txt', 'Secrets/Secrets/ActivationCodes.txt')

    # Main loop to allow processing multiple submarines
    while True:
        # Let the user select a submarine
        selected_serial = select_submarine(submarine_serials)
        selected_submarine = Submarine(selected_serial)
        submarines = {selected_serial: selected_submarine}

        # Load movements for the selected submarine and measure the time
        print(f"\nLaddar rörelser för ubåt {selected_serial}...")
        start_time = time.time()
        selected_submarine.load_movements(f'MovementReports/{selected_serial}.txt')
        end_time = time.time()
        print(f"Rörelser laddade på {end_time - start_time:.2f} sekunder.")

        # Display information about the selected submarine
        print(f"\nUbåt: {selected_submarine.serial_number}")
        print(f"Position: Höjd {selected_submarine.position[0]}, Horisontell {selected_submarine.position[1]}")
        print(f"Totalt antal rörelser: {len(selected_submarine.movement_log)}")
        print("")

        # Ask if the user wants to process other submarines
        bearbeta_andra = input("Vill du bearbeta rörelser för några andra ubåtar för att kontrollera kollisioner och torpedrisk? (j/n): ").lower()
        if bearbeta_andra == 'j':
            try:
                antal_andra_ubatar = int(input("Ange antal andra ubåtar att bearbeta (t.ex. 100): "))
            except ValueError:
                print("Ogiltigt antal. Använder 100 som standard.")
                antal_andra_ubatar = 100

            andra_serialer = [s for s in submarine_serials if s != selected_serial]
            slumpade_serialer = random.sample(andra_serialer, min(antal_andra_ubatar, len(andra_serialer)))

            # Load movements for the selected submarines
            for serial in slumpade_serialer:
                submarine = Submarine(serial)
                submarine.load_movements(f'MovementReports/{serial}.txt')
                submarines[serial] = submarine

            # Check for collisions
            for sub in submarines.values():
                if sub.serial_number != selected_submarine.serial_number:
                    selected_submarine.check_collision(sub)

            # Check torpedo firing
            print("Kontrollerar möjligheten att avfyra torped...")
            directions = ['forward', 'up', 'down']
            for direction in directions:
                can_fire = selected_submarine.can_fire_torpedo(direction, submarines)
                if can_fire:
                    print(f"Ubåten kan avfyra torped {direction} utan risk för friendly fire.")
                else:
                    print(f"Varning: Risk för friendly fire vid avfyrning {direction}.")

            # Find extreme submarines in this subset
            find_extreme_submarines(submarines)

        else:
            print("Ingen ytterligare bearbetning av andra ubåtar.")

        # Process sensor data for the selected submarine
        print(f"\nBearbetar sensordata för ubåt {selected_serial}...")
        sensor_file = f"Sensordata/Sensordata/{selected_serial}.txt"
        if os.path.exists(sensor_file):
            sensor_data = SensorData(sensor_file)
            sensor_data.load_sensor_data()
            sensor_data.count_errors()
            sensor_data.display_repeated_errors()
            sensor_data.log_errors()
        else:
            print("Ingen sensordata tillgänglig för denna ubåt.")
            # Log the missing sensor data
            from logger import log_error
            log_error(f"No sensor data available for submarine {selected_serial}")

        # Activate Nuke for the selected submarine
        print("\nAktiverar Nuke för vald ubåt...")
        secret_manager.activate_nuke(selected_serial)

        # Ask if the user wants to process another submarine or exit
        continue_choice = input("\nVill du analysera en annan ubåt? (j/n): ").lower()
        if continue_choice != 'j':
            print("Avslutar programmet.")
            break

if __name__ == "__main__":
    main()
