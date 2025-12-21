import sys
from urllib.parse import urlparse

# importem els nostres fitxers d'eines
# assegura't que tots els fitxers .py estiguin a la mateixa carpeta
import scanner
import Detect
import headers
import checkInsecureTLSversion
import checkSSLcaducity
import checkSelfsigned

def mostrar_seccio(titol, contingut):
    """
    funció simple per imprimir les dades endreçades a la consola
    """
    print(f"\n{'-'*40}")
    print(f" {titol}")
    print(f"{'-'*40}")
    
    if isinstance(contingut, dict):
        for k, v in contingut.items():
            if isinstance(v, list):
                print(f"{k}:")
                for item in v:
                    print(f"  - {item}")
            elif isinstance(v, dict):
                print(f"{k}:")
                for sub_k, sub_v in v.items():
                    print(f"  - {sub_k}: {sub_v}")
            else:
                print(f"{k}: {v}")
    else:
        print(f"{contingut}")

def main():
    print("Iniciant WebSec Analyzer...")
    
    # demana l'url a l'usuari i treu espais sobrants
    target_url = input("Introdueix l'URL a analitzar: ").strip()
    
    # si l'usuari no posa https l'hi posem nosaltres
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    
    # treu només el nom del domini per a les proves de connexió
    parsed = urlparse(target_url)
    host = parsed.netloc
    
    print(f"\n[+] Analitzant objectiu: {target_url}")
    print("[+] Resultats de l'anàlisi:")
        
    # 1. escàner bàsic de disponibilitat
    print("\n -> Comprovant si la web està activa...")
    scan_res = scanner.analyze_url(target_url)
    
    # preparem les dades perquè es llegeixin bé
    dades_scanner = {
        "Online": "sí" if scan_res.get("alive") else "no",
        "Codi Estat": scan_res.get("status_code"),
        "Latència (temps càrrega)": f"{scan_res.get('load_time')} seg"
    }
    mostrar_seccio("DISPONIBILITAT", dades_scanner)
    
    # si el web no respon parem aquí
    if not scan_res.get("alive"):
        print("❌ ERROR: el servidor no respon. Fi de l'anàlisi")
        return

    # 2. detector de tecnologies
    print("\n -> Cercant tecnologies utilitzades...")
    detect_res = Detect.detect_technologies(target_url)
    
    llista_tech = []
    for t in detect_res.get("technologies", []):
        nom = t.get('name', 'desconegut')
        tipus = t.get('type', 'general')
        ver = t.get('version') or '?'
        llista_tech.append(f"{nom} ({tipus}) v:{ver}")
        
    tech_summary = {
        "Tecnologies detectades": llista_tech if llista_tech else ["no s'ha detectat res específic"]
    }
    mostrar_seccio("TECNOLOGIES", tech_summary)

    # 3. anàlisi de capçaleres
    print("\n -> Revisant capçaleres http...")
    headers_res = headers.analitzar_capcaleres(target_url)
    mostrar_seccio("CAPÇALERES HTTP", headers_res)

    # 4. proves de seguretat ssl (només si és https)
    if target_url.startswith("https"):
        print("\n -> Realitzant proves de seguretat SSL/TLS...")
        
        # prova de versions antigues
        tls_res = checkInsecureTLSversion.verificar_tls_insegur(host)
        mostrar_seccio("PROTOCOLS OBSOLETS", tls_res)
        
        # prova de caducitat
        caducat = checkSSLcaducity.verificar_caducitat_ssl(host)
        mostrar_seccio("ESTAT CERTIFICAT", {"Està caducat?": "sí" if caducat else "no"})
        
        # prova d'autofirmat
        autofirmat = checkSelfsigned.verificar_certificat_autofirmat(host)
        mostrar_seccio("TIPUS DE SIGNATURA", {"És autofirmat?": "sí" if autofirmat else "no"})
    else:
        print("\n[!] Saltant proves SSL perquè el web no utilitza https")

    print("\n✅ Anàlisi completat.")

if __name__ == "__main__":
    main()