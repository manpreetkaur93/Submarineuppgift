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

# Funktion för att lista alla ubåtars serienummer
def list_submarine_serials(folder):
    return [filename.split('.')[0] for filename in os.listdir(folder) if filename.endswith(".txt")]

# Funktion för att låta användaren välja en ubåt genom att ange serienummer
def select_submarine(serials):
    while True:
        serial_number = input("Ange serienumret för den ubåt du vill välja: ")
        if serial_number in serials:
            return serial_number
        else:
            print("Ubåten hittades inte. Försök igen.")

# Funktion för att hitta närmaste och längst bort, högsta och lägsta ubåtar relativt vald ubåt
def find_extreme_submarines_relative_to_selected(submarines, selected_submarine):
    # Exkludera den valda ubåten från jämförelsen
    other_submarines = [sub for sub in submarines.values() if sub.serial_number != selected_submarine.serial_number]
    if not other_submarines:
        print("Inga andra ubåtar att jämföra med.")
        return

    # Beräkna avstånd från den valda ubåten
    def distance_from_selected(sub):
        delta_depth = sub.position[0] - selected_submarine.position[0]
        delta_horizontal = sub.position[1] - selected_submarine.position[1]
        return (delta_depth**2 + delta_horizontal**2) ** 0.5

    sorted_by_distance = sorted(other_submarines, key=distance_from_selected)
    closest_sub = sorted_by_distance[0]
    farthest_sub = sorted_by_distance[-1]
    closest_distance = distance_from_selected(closest_sub)
    farthest_distance = distance_from_selected(farthest_sub)

    # För djup, lägre värde innebär högre upp (mindre djup)
    sorted_by_depth = sorted(other_submarines, key=lambda sub: sub.position[0])
    highest_sub = sorted_by_depth[0]
    lowest_sub = sorted_by_depth[-1]

    print(f"Närmaste ubåt: {closest_sub.serial_number}, Avstånd från vald ubåt: {closest_distance:.2f} meter")
    print(f"Längst bort ubåt: {farthest_sub.serial_number}, Avstånd från vald ubåt: {farthest_distance:.2f} meter")
    print(f"Högsta ubåt: {highest_sub.serial_number}, Höjd: {highest_sub.position[0]} meter")
    print(f"Lägsta ubåt: {lowest_sub.serial_number}, Höjd: {lowest_sub.position[0]} meter")

def main():
    # Se till att nödvändiga mappar finns
    os.makedirs('logs', exist_ok=True)

    # Lista alla ubåtars serienummer
    print("Lister alla ubåtar...")
    submarine_serials = list_submarine_serials('MovementReports')

    # Initiera SecretManager med korrekta filvägar
    secret_manager = SecretManager('Secrets/Secrets/SecretKEY.txt', 'Secrets/Secrets/ActivationCodes.txt')

    # Huvudloop för att tillåta bearbetning av flera ubåtar
    while True:
        # Låt användaren välja en ubåt
        selected_serial = select_submarine(submarine_serials)
        selected_submarine = Submarine(selected_serial)
        submarines = {selected_serial: selected_submarine}

        # Ladda rörelser för den valda ubåten och mät tiden
        print(f"\nLaddar rörelser för ubåt {selected_serial}...")
        start_time = time.time()
        selected_submarine.load_movements(f'MovementReports/{selected_serial}.txt')
        end_time = time.time()
        print(f"Rörelser laddade på {end_time - start_time:.2f} sekunder.")

        # Visa information om den valda ubåten
        print(f"\nUbåt: {selected_submarine.serial_number}")
        print(f"Position: Höjd {selected_submarine.position[0]} meter, Horisontell {selected_submarine.position[1]} meter")
        print(f"Totalt antal rörelser: {len(selected_submarine.movement_log)}")
        print("")

        # Meny för att välja åtgärder
        while True:
            print("\nVälj en åtgärd:")
            print("1. Kontrollera kollisioner och torpedrisk")
            print("2. Analysera sensordata")
            print("3. Aktivera Nuke")
            print("4. Visa närmaste och längst bort, högsta och lägsta ubåtar från vald ubåt")
            print("5. Välj en annan ubåt")
            print("6. Avsluta programmet")
            choice = input("Ange ditt val (1-6): ")

            if choice == '1':
                # Bearbeta andra ubåtar för kollisioner och torpedrisk
                try:
                    antal_andra_ubatar = int(input("Ange antal andra ubåtar att bearbeta (t.ex. 100): "))
                except ValueError:
                    print("Ogiltigt antal. Använder 100 som standard.")
                    antal_andra_ubatar = 100

                andra_serialer = [s for s in submarine_serials if s != selected_serial]
                slumpade_serialer = random.sample(andra_serialer, min(antal_andra_ubatar, len(andra_serialer)))

                # Ladda rörelser för de valda ubåtarna
                for serial in slumpade_serialer:
                    if serial not in submarines:
                        submarine = Submarine(serial)
                        submarine.load_movements(f'MovementReports/{serial}.txt')
                        submarines[serial] = submarine

                # Kontrollera kollisioner
                total_collisions = 0
                for sub in submarines.values():
                    if sub.serial_number != selected_submarine.serial_number:
                        collisions = selected_submarine.check_collision(sub)
                        if collisions:
                            # Exkludera kollisioner på position (0, 0)
                            filtered_collisions = [(pos, time) for pos, time in collisions if pos != (0, 0)]
                            num_collisions = len(filtered_collisions)
                            total_collisions += num_collisions
                            if num_collisions > 0:
                                print(f"Kollisioner upptäckta mellan {selected_submarine.serial_number} och {sub.serial_number}: {num_collisions} st")
                print(f"Totalt antal kollisioner för ubåt {selected_submarine.serial_number}: {total_collisions}")

                # Kontrollera möjligheten att avfyra torped i alla riktningar
                print("Kontrollerar möjligheten att avfyra torped...")
                directions = ['forward', 'up', 'down']
                for direction in directions:
                    can_fire = selected_submarine.can_fire_torpedo(direction, submarines)
                    if can_fire:
                        print(f"Ubåten {selected_serial} kan avfyra torped {direction} utan risk för friendly fire.")
                    else:
                        print(f"Varning: Ubåten {selected_serial} riskerar friendly fire vid avfyrning {direction}!")

            elif choice == '2':
                # Bearbeta sensordata för den valda ubåten
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
                    # Logga avsaknad av sensordata
                    from logger import log_error
                    log_error(f"No sensor data available for submarine {selected_serial}")

            elif choice == '3':
                # Aktivera Nuke för den valda ubåten
                print("\nAktiverar Nuke för vald ubåt...")
                secret_manager.activate_nuke(selected_serial)

            elif choice == '4':
                # Visa närmaste och längst bort, högsta och lägsta ubåtar från vald ubåt
                if len(submarines) > 1:
                    find_extreme_submarines_relative_to_selected(submarines, selected_submarine)
                else:
                    print("Inga andra ubåtar har bearbetats ännu. Välj först att bearbeta andra ubåtar.")

            elif choice == '5':
                # Välj en annan ubåt
                break  # Gå tillbaka till början av huvudloopen

            elif choice == '6':
                print("Avslutar programmet.")
                exit()

            else:
                print("Ogiltigt val. Försök igen.")

if __name__ == "__main__":
    main()
