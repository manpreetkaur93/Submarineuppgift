import os
import logging
from logging.handlers import RotatingFileHandler

# Se till att 'logs' mappen finns
os.makedirs('logs', exist_ok=True)

# Huvudloggern med RotatingFileHandler
error_handler = RotatingFileHandler('logs/submarine_errors.log', maxBytes=1024*1024, backupCount=1)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s %(message)s")
error_handler.setFormatter(error_formatter)

error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

# Rörelselogger med RotatingFileHandler
movement_handler = RotatingFileHandler('logs/movements.log', maxBytes=1024*1024, backupCount=1)
movement_handler.setLevel(logging.INFO)
movement_formatter = logging.Formatter("%(asctime)s %(message)s")
movement_handler.setFormatter(movement_formatter)

movement_log = logging.getLogger('movements')
movement_log.setLevel(logging.INFO)
movement_log.addHandler(movement_handler)

def movement_logger(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        movement = f"{func.__name__} {args[0]}" if args else func.__name__
        movement_log.info(f"Ubåt {self.serial_number} utförde rörelse: {movement}")
        return result
    return wrapper

def log_error(error_message):
    error_logger.error(error_message)

def log_collision(submarine1, submarine2):
    log_error(f"Kollision upptäckt mellan {submarine1.serial_number} och {submarine2.serial_number}")
