import os
import time
from submarine import Submarine
from sensor_data import SensorData
from secret_manager import SecretManager

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

# Funktion för att lista alla ubåtars serienummer
def list_submarine_serials(folder):
    serials = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            serial_number = filename.split('.')[0]
            serials.append(serial_number)
    return serials

# Låta användaren välja en ubåt genom att ange serienummer
def select_submarine(serials):
    while True:
        serial_number = input("Ange serienumret för den ubåt du vill välja: ")
        if serial_number in serials:
            return serial_number
        else:
            print("Ubåten hittades inte. Försök igen.")

# Visa information om den valda ubåten
def display_submarine_info(submarine):
    print(f"\nUbåt: {submarine.serial_number}")
    print(f"Position: Höjd {submarine.position[0]}, Horisontell {submarine.position[1]}")
    print(f"Totalt antal rörelser: {len(submarine.movement_log)}")
    print("")

# Huvudfunktionen
def main():
    # Skapa nödvändiga mappar om de inte redan finns
    os.makedirs('logs', exist_ok=True)

    # Lista alla ubåtars serienummer
    print("Lister alla ubåtar...")
    submarine_serials = list_submarine_serials('MovementReports')

    # Låt användaren välja en ubåt
    selected_serial = select_submarine(submarine_serials)
    selected_submarine = Submarine(selected_serial)

    # Ladda rörelser för den valda ubåten och mät tiden
    print(f"\nLaddar rörelser för ubåt {selected_serial}...")
    start_time = time.time()
    selected_submarine.load_movements(f'MovementReports/{selected_serial}.txt')
    end_time = time.time()
    print(f"Rörelser laddade på {end_time - start_time:.2f} sekunder.")

    # Visa information om den valda ubåten
    display_submarine_info(selected_submarine)

    # Bearbeta sensordata för den valda ubåten
    print(f"Bearbetar sensordata för ubåt {selected_serial}...")
    sensor_file = f"Sensordata/Sensordata/{selected_serial}.txt"
    if os.path.exists(sensor_file):
        sensor_data = SensorData(sensor_file)
        sensor_data.load_sensor_data()
        sensor_data.count_errors()
        sensor_data.display_repeated_errors()
        sensor_data.log_errors()
    else:
        print("Ingen sensordata tillgänglig för denna ubåt.")

    # Aktivera Nuke för den valda ubåten
    print("\nAktiverar Nuke för vald ubåt...")
    secret_manager = SecretManager('Secrets/Secrets/SecretKEY.txt', 'Secrets/Secrets/ActivationCodes.txt')
    secret_manager.activate_nuke(selected_serial)

if __name__ == "__main__":
    main()
