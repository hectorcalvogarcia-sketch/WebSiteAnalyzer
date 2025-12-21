import ssl
import socket
host = "enti.com"

# La funcio rep el nom del host (wikipedia.com) i el port (per defecte 443)
def is_self_signed_certificate(host, port=443):
    # Creem un context SSL per a la connexió
    context = ssl.create_default_context()
    context.check_hostname = True
    # Exigim la verificació del certificat
    context.verify_mode = ssl.CERT_REQUIRED
    # Intentem establir una connexió SSL/TLS
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                # Si la connexió es exitosa, el certificat no és autofirmat
                    return False
    except ssl.SSLCertVerificationError as e:
        # Si hi ha un error de verificació del certificat, comprovem si és un certificat autofirmat
        if "self signed" in str(e).lower() or "certificate verify failed" in str(e).lower():
            return True
        return False # Si és un altre tipus d'error de verificació, retornem False
    except Exception:
        return False


print(is_self_signed_certificate(host))