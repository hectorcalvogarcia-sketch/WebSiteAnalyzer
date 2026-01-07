from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def calcular_puntuacio_global(resultat: dict) -> int:
    puntuacio = 100

    # Si no està online, 0 directe
    if not resultat.get("alive", False):
        return 0

    # Penalitzacions
    status = resultat.get("status_code", 0)
    if status != 200: puntuacio -= 20

    load_time = resultat.get("load_time", 0)
    if isinstance(load_time, (int, float)) and load_time > 3: puntuacio -= 10

    if resultat.get("tls_insecure", False): puntuacio -= 30

    cert_info = resultat.get("certificate", {})
    if cert_info.get("expired", False) or resultat.get("cert_expired", False): puntuacio -= 30

    if resultat.get("self_signed", False): puntuacio -= 15

    # Penalització per CVEs (Vulnerabilitats)
    cves_dict = resultat.get("cves", {})
    if cves_dict:
        puntuacio -= 30 # Si en té, baixa nota

    # Penalització SQL Injection
    if resultat.get("sqli_vuln", False):
        puntuacio -= 50

    return max(0, min(100, puntuacio))

def classificar_risc(puntuacio: int) -> str:
    if puntuacio >= 80: return "Baix"
    elif puntuacio >= 50: return "Mitjà"
    elif puntuacio >= 20: return "Alt"
    else: return "Crític"

def check_page_break(c, y):
    """Mira si ens hem quedat sense espai i crea una pàgina nova"""
    if y < 3 * cm:
        c.showPage()
        c.setFont("Helvetica", 10)
        return 29.7 * cm - 3 * cm # Tornem a dalt
    return y

def generate_pdf_report(resultat: dict, filename: str) -> None:
    print(f"--- GENERANT PDF COMPLET A: {filename} ---")
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 4 * cm

    # --- PÀGINA 1: PORTADA ---
    c.setFont("Helvetica-Bold", 24)
    c.drawString(2 * cm, height - 3 * cm, "Informe d'Anàlisi Web")
    
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, height - 4.5 * cm, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(2 * cm, height - 5.2 * cm, f"URL: {resultat.get('url', '')}")

    puntuacio = calcular_puntuacio_global(resultat)
    nivell = classificar_risc(puntuacio)

    # Nota gran
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 8 * cm, f"Puntuació Global: {puntuacio}/100")
    c.drawString(2 * cm, height - 9 * cm, f"Nivell de Risc: {nivell}")
    
    # Resum bàsic
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 12 * cm, "Resum d'Estat")
    c.setFont("Helvetica", 12)
    alive = resultat.get("alive", False)
    c.drawString(2 * cm, height - 13 * cm, f"- Estat: {'ONLINE' if alive else 'OFFLINE'}")
    c.drawString(2 * cm, height - 14 * cm, f"- Codi HTTP: {resultat.get('status_code', 'N/A')}")
    c.drawString(2 * cm, height - 15 * cm, f"- Temps resposta: {resultat.get('load_time', 'N/A')} s")

    c.showPage() # Saltem pàgina per posar els detalls

    # --- PÀGINA 2: DETALLS TÈCNICS ---
    y = height - 3 * cm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "Detalls de Tecnologies i Vulnerabilitats")
    y -= 1.5 * cm
    c.setFont("Helvetica", 10)

    # 1. Tecnologies detectades
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Tecnologies Detectades:")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)
    
    techs = resultat.get("technologies", [])
    if not techs:
        c.drawString(2.5 * cm, y, "No s'han detectat tecnologies específiques.")
        y -= 0.6 * cm
    else:
        for t in techs:
            txt = f"• {t.get('name')} (v{t.get('version') or '?'}) - {t.get('type')}"
            c.drawString(2.5 * cm, y, txt)
            y -= 0.5 * cm
    
    y -= 0.5 * cm
    
    # 2. Llista de CVEs (EL QUE ET FALTAVA!)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Vulnerabilitats Conegudes (CVEs):")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)

    cves = resultat.get("cves", {})
    if not cves:
        c.drawString(2.5 * cm, y, "No s'han trobat CVEs coneguts.")
        y -= 0.6 * cm
    else:
        for tech, llista_vulns in cves.items():
            # Títol del software (ex: nginx 1.19.0)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(2.5 * cm, y, f"Producte: {tech}")
            y -= 0.5 * cm
            c.setFont("Helvetica", 9)
            
            # Llista de cadascun dels CVEs
            for v in llista_vulns:
                # Si no queda espai, crea pàgina nova
                y = check_page_break(c, y)
                
                cve_id = v.get('cve', 'N/A')
                severity = v.get('severity', 'Unknown')
                score = v.get('score', 0)
                
                # Pintem vermell si és greu
                if score >= 9.0: c.setFillColorRGB(0.8, 0, 0)
                else: c.setFillColorRGB(0, 0, 0)
                
                c.drawString(3 * cm, y, f"- {cve_id} | Severitat: {severity} ({score})")
                y -= 0.4 * cm
            
            y -= 0.3 * cm # Espai entre grups
            c.setFillColorRGB(0, 0, 0) # Tornem a negre

    # 3. SQL Injection i Altres
    y -= 1 * cm
    y = check_page_break(c, y)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Altres Proves:")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)

    if resultat.get("sqli_vuln"):
        c.setFillColorRGB(1, 0, 0)
        c.drawString(2.5 * cm, y, "CRÍTIC: Vulnerabilitat SQL Injection detectada!")
    else:
        c.setFillColorRGB(0, 0.5, 0)
        c.drawString(2.5 * cm, y, "Segur: No s'ha detectat SQL Injection.")
    
    y -= 0.5 * cm
    c.setFillColorRGB(0, 0, 0)
    
    if resultat.get("cert_expired"):
        c.drawString(2.5 * cm, y, "AVÍS: Certificat SSL caducat.")
    if resultat.get("self_signed"):
        c.drawString(2.5 * cm, y, "AVÍS: Certificat autofirmat.")

    c.save()