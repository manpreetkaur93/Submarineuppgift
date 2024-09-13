# secret_manager.py
import hashlib
import datetime

class SecretManager:
    def __init__(self, secret_key_file, activation_code_file):
        self.secret_key_file = secret_key_file
        self.activation_code_file = activation_code_file
        self.keys = self.load_secrets(secret_key_file)
        self.activation_codes = self.load_secrets(activation_code_file)

    def load_secrets(self, filepath):
        secrets = {}
        with open(filepath, 'r') as file:
            for line in file:
                serial, key = line.split(':')
                secrets[serial.strip()] = key.strip()
        return secrets

    def activate_nuke(self, serial_number):
        if serial_number in self.keys and serial_number in self.activation_codes:
            secret_key = self.keys[serial_number]
            activation_code = self.activation_codes[serial_number]
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            combined_string = date_str + secret_key + activation_code
            activation_hash = hashlib.sha256(combined_string.encode()).hexdigest()
            print(f"Nuke activation hash for {serial_number}: {activation_hash}")
        else:
            print(f"No keys or activation codes found for submarine {serial_number}")
