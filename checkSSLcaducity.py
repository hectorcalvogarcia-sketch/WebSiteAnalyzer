import ssl
import socket
from datetime import datetime
host = "chatgpt.com"

def check_certificate_validity(host, port=443):
    # Creem un context SSL per a la connexió i desactivem la verificació del certificat per permetre l'obtenció de certificats caducats
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_OPTIONAL
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        if not cert or 'notAfter' not in cert:
            return True  # Si no es pot obtenir el certificat, considerem que està caducat

        expiration_date = cert['notAfter']
        expiration_date_formatted = datetime.strptime(expiration_date, '%b %d %H:%M:%S %Y %Z')
    
        current_date = datetime.utcnow()
        # si la data actual es mes gran que la data de caducitat, el certificat ha caducat
        return True if expiration_date_formatted < current_date else False
    except ssl.SSLError:
        return True  # Si hi ha un error SSL, considerem que el certificat està caducat o no vàlid

print(check_certificate_validity(host))