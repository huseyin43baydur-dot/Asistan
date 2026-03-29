import os
import hashlib
import socket
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='security_log.log', format='%(asctime)s - %(levelname)s - %(message)s')

class VirusProtection:
    def __init__(self):
        self.blocked_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 5432]
        self.suspicious_files = []

    def detect_malware(self, file_path):
        """Check if the file is malicious based on its hash."""
        known_malware_hashes = {  # Replace with actual known malware hashes
            'd41d8cd98f00b204e9800998ecf8427e': 'Example Malware 1',
            '5f4dcc3b5aa765d61d8327deb882cf99': 'Example Malware 2'
        }
        file_hash = self.hash_file(file_path)
        if file_hash in known_malware_hashes:
            logging.warning(f'Malware detected: {known_malware_hashes[file_hash]} in {file_path}')
            return True
        return False

    def hash_file(self, file_path):
        """Generate SHA-256 hash of the file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def monitor_network(self):
        """Monitor network connections for suspicious activity."""
        logging.info('Monitoring network connections...')
        for port in self.blocked_ports:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            if f':{port} ' in result.stdout:
                logging.warning(f'Blocked port {port} is open!')

    def validate_input(self, user_input):
        """Validate input for potential injection attacks."""
        if isinstance(user_input, str) and user_input.isalnum():
            logging.info('Input validation passed.')
            return True
        logging.warning('Input validation failed.')
        return False

    def protect_file_system(self, directory):
        """Protect the file system from unauthorized access."""
        logging.info('Scanning directory for suspicious files...')
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                if self.detect_malware(full_path):
                    self.suspicious_files.append(full_path)
                    logging.warning(f'Suspicious file detected: {full_path}')  

if __name__ == '__main__':
    virus_protection = VirusProtection()
    virus_protection.monitor_network()
    virus_protection.protect_file_system('/')  # Change to a specific directory as needed
