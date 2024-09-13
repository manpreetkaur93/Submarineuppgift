# logger.py

import logging

# Setup logger
logging.basicConfig(filename="submarine_errors.log", level=logging.ERROR,
                    format="%(asctime)s %(message)s")

def log_error(error_message):
    logging.error(error_message)

def log_collision(submarine1, submarine2):
    log_error(f"Collision detected between {submarine1.serial_number} and {submarine2.serial_number}")
