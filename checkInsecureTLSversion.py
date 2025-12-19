import requests
import ssl
import socket
host = "enti.cat"
#url = "https://tls-v1-0.badssl.com:1010/"
def insecure_tls_version(host, port=443):
    #La funcio rep el nom del host (wikipedia.com) i el port (per defecte 443)

    #Creem un diccionari per guardar els resultats, per defecte tots dos valen False
    results = {
        'TLSv1.0': False,
        'TLSv1.1': False
    }
    # Creem un diccionari amb els protocols TLS que volem comprovar
    tls_versions = {
        'TLSv1.0': ssl.PROTOCOL_TLSv1,
        'TLSv1.1': ssl.PROTOCOL_TLSv1_1
    }
    for version_name, protocol in tls_versions.items():
        # Intentem guardar el context SSL per a cada versió, que es el conjunt de paràmetres i opcions que s'utilitzen per a la connexió SSL/TLS
        try:
            context = ssl.SSLContext(protocol)
            context.set_ciphers("ALL:@SECLEVEL=0")  # Permet tots els xifrats

            # Creem un socket, que es una conexió de xarxa, cap a el host i port especificats. Li donem un timeout de 5 segons per tallar la connexió si no es pot establir
            with socket.create_connection((host, port), timeout=5) as sock:
                # Intentem establir una connexió SSL/TLS utilitzant el context creat anteriorment
                with context.wrap_socket(sock, server_hostname=host):
                    # Si la connexió es exitosa, marquem aquesta versió de TLS com a suportada
                    results[version_name] = True

        except ssl.SSLError:
            # Si hi ha un error SSL, significa que aquesta versió de TLS no es suportada
            pass
        except Exception:
            #Si hi ha qualsevol altre tipus d'error, el ignorem
            pass
    return results
        

print(insecure_tls_version(host))