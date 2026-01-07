import tkinter as tk
from urllib.parse import urlparse
import logging
import os

import src.scanners.scanner as scanner, src.scanners.Detect as Detect, src.scanners.headers as headers, src.scanners.checkInsecureTLSversion as checkInsecureTLSversion
import src.scanners.checkSSLcaducity as checkSSLcaducity, src.scanners.checkSelfsigned as checkSelfsigned, src.scanners.cve_correlation as cve_correlation, src.scanners.sqli_scan as sqli_scan
from src.utils import report_pdf

basedir = os.getcwd()# directori base del projecte
logdir = os.path.join(basedir, "logs")
log_file = os.path.join(logdir, "websec.log")
try:
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
except Exception as e:
    print(f"Error configurant el registre de logs: {e}")

dades_informe = {}

def escriure(text_area, text):
    """Escriu el text i FORÇA la finestra a actualitzar-se"""
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, str(text) + "\n")
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)
    text_area.update() 

def executar_escaner(url, text_area):
    global dades_informe
    logging.info(f"Iniciant escaneig: {url}")
    dades_informe.clear()
    dades_informe["url"] = url
    dades_informe["alive"] = False
    # 1. Preparació
    escriure(text_area, f"Analitzant: {url} ...")
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        parsed = urlparse(url)
        host = parsed.netloc
    except:
        escriure(text_area, "URL invàlida.")
        logging.error(f"URL invàlida: {url}")
        return

    # 2. Disponibilitat
    escriure(text_area, "\n[1] Mirant si està online...")
    try:
        res = scanner.analyze_url(url)
        dades_informe.update(res)  # Guardem els resultats a les dades de l'informe
        if res.get("alive"):
            escriure(text_area, f" -> OK. Codi: {res.get('status_code')}")
            logging.info(f"Web online: {url} (Codi: {res.get('status_code')})")
        else:
            escriure(text_area, " -> El web no respon.")
            logging.warning(f"El web no respon: {url}")
            return # Parem si no va
    except Exception as e:
        escriure(text_area, f"Error: {e}")
        logging.error(f"Error en analitzar disponibilitat: {e}")

    # 3. Tecnologies
    escriure(text_area, "\n[2] Detectant tecnologies...")
    try:
        techs = Detect.detect_technologies(url)
        dades_informe["technologies"] = techs.get("technologies", [])
        llista = {}
        # Fem un bucle simple per mostrar-ho
        count_tech = 0
        for t in techs.get("technologies", []):
            nom = t.get('name')
            ver = t.get('version') or '?'
            escriure(text_area, f" -> {nom} (v{ver})")
            logging.info(f"Tecnologia trobada: {nom} v{ver}")
            if nom: llista[nom.lower()] = ver
            count_tech +=1
        if count_tech == 0:
            escriure(text_area, " -> Cap tecnologia detectada.")
            logging.info(f"No s'han detectat tecnologies")
        # CVEs (si n'hi ha)
        if llista:
            escriure(text_area, "\n   [>] Buscant vulnerabilitats CVE...")
            cves = cve_correlation.search_cve(llista)
            dades_informe["cves"] = cves
            if cves:
                logging.warning(f"S'han trobat CVEs per a: {list(cves.keys())}")
            else:
                logging.info(f"No s'han trobat CVEs associats a les tecnologies detectades")
            for k, v in cves.items():
                escriure(text_area, f"    - {k}: {v}")
    except Exception as e:
        escriure(text_area, f"Error Tech: {e}")
        logging.error(f"Error en detectar tecnologies: {e}")

    # 4. Headers
    escriure(text_area, "\n[3] Headers HTTP...")
    try:
        caps = headers.analitzar_capcaleres(url)
        dades_informe["headers"] = caps
        for k, v in caps.items():
            escriure(text_area, f" -> {k}: {v}")
        logging.info(f"Headers analitzats per: {url}")
    except Exception as e:
        escriure(text_area, f"Error Headers: {e}")
        logging.error(f"Error en analitzar headers: {e}")

    # 5. SSL (Només si és https)
    if "https" in url:
        escriure(text_area, "\n[4] Seguretat SSL...")
        try:
            caducat = checkSSLcaducity.verificar_caducitat_ssl(host)
            auto = checkSelfsigned.verificar_certificat_autofirmat(host)
            insegur_dict = checkInsecureTLSversion.verificar_tls_insegur(host)
            
            dades_informe["cert_expired"] = caducat
            dades_informe["self_signed"] = auto
            dades_informe["tls_insecure"] = any(insegur_dict.values())
            
            escriure(text_area, f" -> Caducat: {'SÍ' if caducat else 'No'}")
            escriure(text_area, f" -> Autofirmat: {'SÍ' if auto else 'No'}")
            if caducat:
                logging.WARNING(f"Certificat SSL caducat a: {url}")
            if auto:
                logging.WARNING(f"Certificat SSL autofirmat a: {url}")
            if not caducat and not auto:
                logging.info(f"Certificat SSL vàlid a: {url}")
        except Exception as e:
            escriure(text_area, f"Error SSL: {e}")
            logging.error(f"Error en analitzar SSL: {e}")

    # 6. SQL Injection
    escriure(text_area, "\n[5] SQL Injection (espera uns segons)...")
    logging.info(f"Iniciant escaneig SQLi per: {url}")
    try:
        # Això pot tardar una mica, la finestra semblarà congelada breument
        sqli = sqli_scan.escaner_sqli(url)
        dades_informe["sqli_vuln"] = sqli["vulnerable"]
        dades_informe["sqli_bugs"] = sqli["bugs"]
        if sqli["vulnerable"]:
            escriure(text_area, " -> ❌ VULNERABLE A SQLI!")
            logging.critical(f"Vulnerabilitat SQLi trobada a: {url}")
        else:
            escriure(text_area, " -> ✅ Cap error SQL trobat.")
    except Exception as e:
        escriure(text_area, f"Error SQL: {e}")

    escriure(text_area, "\n✅ Finalitzat.")
    logging.info(f"Escaneig finalitzat")


def generar_pdf_logic(filename):
    """Aquesta funció crida al mòdul report_pdf amb les dades que hem recollit"""
    # Si l'usuari intenta guardar sense haver escanejat res
    if not dades_informe:
        logging.warning("Intent de generar informe PDF sense dades")
        return False, "No hi ha dades"
    
    if "alive" not in dades_informe:
        dades_informe["alive"] = False
    try:
        # Cridem al fitxer report_pdf.py que tens a src/utils/
        report_pdf.generate_pdf_report(dades_informe, filename)
        logging.info(f"Informe PDF generat: {filename}")
        return True, f"Informe guardat a: {filename}"
    except Exception as e:
        logging.error(f"Error generant PDF: {e}")
        return False, f"Error generant PDF: {str(e)}"