import ssl
import socket

def verificar_certificat_autofirmat(host, port=443): # esbrina si el certificat se l'han fet ells mateixos retorna true si és autofirmat, false si és de confiança
    # prepara una connexió exigent que ho verifiqui tot
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    
    try:
        # intenta connectar de forma segura estàndard
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                # si no hi ha error, és que el certificat és oficial
                return False
    except ssl.SSLCertVerificationError as e:
        # si falla, mirem si és perquè és autofirmat
        error_str = str(e).lower()
        if "self signed" in error_str or "certificate verify failed" in error_str:
            return True 
        return False
    except:
        # si és un altre error no podem assegurar res
        return False