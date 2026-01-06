import tkinter as tk
from urllib.parse import urlparse

import scanner, Detect, headers, checkInsecureTLSversion
import checkSSLcaducity, checkSelfsigned, cve_correlation, sqli_scan


def escriure(text_area, text):
    """Escriu el text i FORÇA la finestra a actualitzar-se"""
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, str(text) + "\n")
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)
    
    # TRUC IMPORTANT: Això fa que el text surti al moment
    # sense necessitat de fils (threads) ni coses complexes.
    text_area.update() 

def executar_escaner(url, text_area):
    
    # 1. Preparació
    escriure(text_area, f"Analitzant: {url} ...")
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        parsed = urlparse(url)
        host = parsed.netloc
    except:
        escriure(text_area, "URL invàlida.")
        return

    # 2. Disponibilitat
    escriure(text_area, "\n[1] Mirant si està online...")
    try:
        res = scanner.analyze_url(url)
        if res.get("alive"):
            escriure(text_area, f" -> OK. Codi: {res.get('status_code')}")
        else:
            escriure(text_area, " -> El web no respon.")
            return # Parem si no va
    except Exception as e:
        escriure(text_area, f"Error: {e}")

    # 3. Tecnologies
    escriure(text_area, "\n[2] Detectant tecnologies...")
    try:
        techs = Detect.detect_technologies(url)
        llista = {}
        # Fem un bucle simple per mostrar-ho
        for t in techs.get("technologies", []):
            nom = t.get('name')
            ver = t.get('version') or '?'
            escriure(text_area, f" -> {nom} (v{ver})")
            if nom: llista[nom.lower()] = ver
        
        # CVEs (si n'hi ha)
        if llista:
            escriure(text_area, "\n   [>] Buscant vulnerabilitats CVE...")
            cves = cve_correlation.search_cve(llista)
            for k, v in cves.items():
                escriure(text_area, f"    - {k}: {v}")
    except Exception as e:
        escriure(text_area, f"Error Tech: {e}")

    # 4. Headers
    escriure(text_area, "\n[3] Headers HTTP...")
    try:
        caps = headers.analitzar_capcaleres(url)
        for k, v in caps.items():
            escriure(text_area, f" -> {k}: {v}")
    except: pass

    # 5. SSL (Només si és https)
    if "https" in url:
        escriure(text_area, "\n[4] Seguretat SSL...")
        try:
            caducat = checkSSLcaducity.verificar_caducitat_ssl(host)
            escriure(text_area, f" -> Caducat: {'SÍ' if caducat else 'No'}")
            
            auto = checkSelfsigned.verificar_certificat_autofirmat(host)
            escriure(text_area, f" -> Autofirmat: {'SÍ' if auto else 'No'}")
        except: pass

    # 6. SQL Injection
    escriure(text_area, "\n[5] SQL Injection (espera uns segons)...")
    try:
        # Això pot tardar una mica, la finestra semblarà congelada breument
        sqli = sqli_scan.escaner_sqli(url)
        if sqli["vulnerable"]:
            escriure(text_area, " -> ❌ VULNERABLE A SQLI!")
            escriure(text_area, str(sqli["bugs"]))
        else:
            escriure(text_area, " -> ✅ Cap error SQL trobat.")
    except Exception as e:
        escriure(text_area, f"Error SQL: {e}")

    escriure(text_area, "\n✅ Finalitzat.")