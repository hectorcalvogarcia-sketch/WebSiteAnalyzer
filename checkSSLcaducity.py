import ssl
import socket
from datetime import datetime

def verificar_caducitat_ssl(host, port=443): # comprova si el certificat de seguretat ha caducat, retorna true si està caducat, false si està bé
    # crea una configuració bàsica que no verifiqui res encara
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_OPTIONAL
    
    try:
        # connecta i demana el certificat al servidor
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        # si no hi ha certificat o no té data, assumim que està caducat
        if not cert or 'notAfter' not in cert:
            return True 

        # converteix la data del certificat a un format entenedor
        fmt = '%b %d %H:%M:%S %Y %Z'
        data_expiracio = datetime.strptime(cert['notAfter'], fmt)
        
        # mira si la data actual és posterior a la de caducitat
        return datetime.utcnow() > data_expiracio
        
    except:
        # si dona error en connectar assumim que no és vàlid
        return True