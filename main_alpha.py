import sys
from urllib.parse import urlparse

# importem els mòduls del projecte
# assegura't que tots els fitxers .py es troben al mateix directori
import scanner
import Detect
import headers
import checkInsecureTLSversion
import checkSSLcaducity
import checkSelfsigned
import cve_correlation
import sqli_scan  

def mostrar_seccio(titol, contingut):
    """
    funció auxiliar per formatar i imprimir els resultats a la consola
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
    
    # sol·licita l'url a l'usuari i elimina espais innecessaris
    target_url = input("Introdueix l'URL a analitzar: ").strip()
    
    # afegeix el protocol https automàticament si no s'especifica
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    
    # extreu el domini principal per a les proves de connexió
    parsed = urlparse(target_url)
    host = parsed.netloc
    
    print(f"\n[+] Analitzant objectiu: {target_url}")
    print("[+] Resultats de l'anàlisi:")
        
    # 1. escàner bàsic de disponibilitat
    print("\n -> Comprovant si la web està activa...")
    scan_res = scanner.analyze_url(target_url)
    
    # estructura les dades per a una lectura clara
    dades_scanner = {
        "Online": "sí" if scan_res.get("alive") else "no",
        "Codi Estat": scan_res.get("status_code"),
        "Latència (temps càrrega)": f"{scan_res.get('load_time')} seg"
    }
    mostrar_seccio("DISPONIBILITAT", dades_scanner)
    
    # atura l'execució si el servidor no respon
    if not scan_res.get("alive"):
        print("❌ ERROR: el servidor no respon. Fi de l'anàlisi")
        return

    # 2. detector de tecnologies
    print("\n -> Cercant tecnologies utilitzades...")
    detect_res = Detect.detect_technologies(target_url)
    
    llista_tech = {}
    for t in detect_res.get("technologies", []):
        nom = t.get('name', 'desconegut')
        tipus = t.get('type', 'general')
        ver = t.get('version') or '?'
        if nom:
            llista_tech[nom.lower()] = ver
        
    tech_summary = {
        "Tecnologies detectades": llista_tech if llista_tech else ["no s'ha detectat res específic"]
    }
    mostrar_seccio("TECNOLOGIES", tech_summary)

    # cerca de cves associats a les tecnologies trobades
    if llista_tech:
        print("\n -> Cercant vulnerabilitats conegudes (CVE)...")
        cve_cve_results = cve_correlation.search_cve(llista_tech)
        mostrar_seccio("VULNERABILITATS CVE", cve_cve_results)
    else:
        print("\n[!] No s'han detectat tecnologies, saltant cerca de CVEs")

    # 3. anàlisi de capçaleres
    print("\n -> Revisant capçaleres http...")
    headers_res = headers.analitzar_capcaleres(target_url)
    mostrar_seccio("CAPÇALERES HTTP", headers_res)

    # 4. proves de seguretat ssl (només si s'utilitza https)
    if target_url.startswith("https"):
        print("\n -> Realitzant proves de seguretat SSL/TLS...")
        
        # verificació de protocols antics
        tls_res = checkInsecureTLSversion.verificar_tls_insegur(host)
        mostrar_seccio("PROTOCOLS OBSOLETS", tls_res)
        
        # verificació de caducitat del certificat
        caducat = checkSSLcaducity.verificar_caducitat_ssl(host)
        mostrar_seccio("ESTAT CERTIFICAT", {"Està caducat?": "sí" if caducat else "no"})
        
        # verificació de certificat autofirmat
        autofirmat = checkSelfsigned.verificar_certificat_autofirmat(host)
        mostrar_seccio("TIPUS DE SIGNATURA", {"És autofirmat?": "sí" if autofirmat else "no"})
    else:
        print("\n[!] Saltant proves SSL perquè el web no utilitza https")

    # 5. escàner d'injecció sql
    print("\n -> Buscant vulnerabilitats d'SQL Injection...")
    sqli_res = sqli_scan.escaner_sqli(target_url)
    
    if sqli_res["vulnerable"]:
        mostrar_seccio("SQL INJECTION TROBAT", {"Estat": "VULNERABLE ❌", "Detalls": sqli_res["bugs"]})
    else:
        mostrar_seccio("SQL INJECTION", {"Estat": "Segur (aparentment) ✅", "Info": sqli_res.get("info", "cap error detectat")})

    print("\n✅ Anàlisi completat.")

if __name__ == "__main__":
    main()