import os
import gdown
import zipfile
import time  # Import för att lägga till fördröjning
from submarine import load_all_movements
from sensor_data import process_all_sensors
from secret_manager import SecretManager

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
    if not os.path.exists('Secrets'):
        os.makedirs('Secrets')
    if not os.path.exists('Sensordata'):
        os.makedirs('Sensordata')
    if not os.path.exists('MovementReports'):
        os.makedirs('MovementReports')

    # Ladda ner och packa upp endast om zip-filerna inte redan finns
    if not os.path.exists('Secrets\Secrets\SecretKEY.txt'):
        print("Downloading Secrets...")
        gdown.download(SECRETS_URL, 'Secrets\secrets.zip', quiet=False)
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

def main():
    # Ladda ner alla filer från Google Drive om de inte redan finns
    download_files()

    # Hantera ubåtsrörelser
    print("Loading all submarine movements...")
    submarines = load_all_movements('MovementReports')

    # Hantera sensorfel
    print("Processing all sensor data...")
    process_all_sensors('Sensordata')

    # Hantera aktivering av Nuke
    print("Activating Nuke for submarine...")
    secret_manager = SecretManager('Secrets/Secrets/SecretKEY.txt', 'Secrets/Secrets/ActivationCodes.txt')
    secret_manager.activate_nuke('10053472-25')

if __name__ == "__main__":
    main()
