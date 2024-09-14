import os
import logging

# Se till att 'logs' mappen finns
os.makedirs('logs', exist_ok=True)

# Konfigurera logger
logging.basicConfig(filename="logs/submarine_errors.log", level=logging.ERROR,
                    format="%(asctime)s %(message)s")

def log_error(error_message):
    logging.error(error_message)

def log_collision(submarine1, submarine2):
    log_error(f"Kollision upptäckt mellan {submarine1.serial_number} och {submarine2.serial_number}")
