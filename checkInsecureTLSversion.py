import ssl
import socket

def verificar_tls_insegur(host, port=443): # mira si el servidor accepta connexions velles i insegures
    # per defecte ho marquem tot com a segur
    resultats = {'TLSv1.0': False, 'TLSv1.1': False}
    
    # llista de versions antigues que no s'haurien de fer servir
    versions_tls = {
        'TLSv1.0': ssl.PROTOCOL_TLSv1,
        'TLSv1.1': ssl.PROTOCOL_TLSv1_1
    }
    
    # prova cada versió una per una
    for nom_versio, protocol in versions_tls.items():
        try:
            # configura la connexió forçant la versió antiga
            context = ssl.SSLContext(protocol)
            context.set_ciphers("ALL:@SECLEVEL=0") # baixa la seguretat al mínim per provar
            
            # intenta connectar
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host):
                    # si connecta, és que accepta la versió insegura
                    resultats[nom_versio] = True
        except:
            # si falla la connexió és bon senyal
            pass
            
    return resultats