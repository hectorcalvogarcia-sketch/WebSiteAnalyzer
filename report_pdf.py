from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def calcular_puntuacio_global(resultat: dict) -> int:
    puntuacio = 100

    # Disponibilitat
    if not resultat.get("alive", False):
        return 0

    status = resultat.get("status_code", 0)
    if status != 200:
        puntuacio -= 20

    # Rendiment
    load_time = resultat.get("load_time", 0)
    if isinstance(load_time, (int, float)) and load_time > 3:
        puntuacio -= 10

    # TLS insegur
    if resultat.get("tls_insecure", False):
        puntuacio -= 30

    # Certificat caducat
    cert_info = resultat.get("certificate", {})
    if cert_info.get("expired", False) or resultat.get("cert_expired", False):
        puntuacio -= 30

    # Certificat autosignat
    if resultat.get("self_signed", False):
        puntuacio -= 15

    # Versions en EoL / sense suport
    eol_list = resultat.get("eol", [])
    penalitzacio_eol = 0
    for item in eol_list:
        status = item.get("status")
        if status in ("EOL", "NO_SUPPORT"):
            penalitzacio_eol += 20
    puntuacio -= min(penalitzacio_eol, 40)

    # Fuites / leaks
    if resultat.get("has_leaks", False):
        puntuacio -= 40

    # Limitar entre 0 i 100
    return max(0, min(100, puntuacio))
def classificar_risc(puntuacio: int) -> str:
    if puntuacio >= 80:
        return "Baix"
    elif puntuacio >= 50:
        return "Mitjà"
    elif puntuacio >= 20:
        return "Alt"
    else:
        return "Crític"

def generate_pdf_report(resultat: dict, filename: str) -> None:
    # Crear el canvas del PDF amb mida A4
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "Informe d'Anàlisi Web")

    c.setFont("Helvetica", 12)
    data = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawString(2 * cm, height - 3.5 * cm, f"Data de l'informe: {data}")
    c.drawString(2 * cm, height - 4.5 * cm, f"URL analitzada: {resultat.get('url', '')}")

    # Càlcul i mostra de la puntuació global
    puntuacio = calcular_puntuacio_global(resultat)
    nivell_risc = classificar_risc(puntuacio)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 6 * cm,
                 f"Puntuació global: {puntuacio}/100")
    c.drawString(2 * cm, height - 7 * cm,
                 f"Nivell de risc: {nivell_risc}")
    # Passar a una nova pàgina
    c.showPage()

    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "Troballes detallades")

    y = height - 3.5 * cm
    line_height = 0.8 * cm
    c.setFont("Helvetica", 12)

    alive = resultat.get("alive", False)
    status_code = resultat.get("status_code", "N/A")
    load_time = resultat.get("load_time", "N/A")

    # Estat general de disponibilitat
    c.drawString(2 * cm, y, f"Estat de disponibilitat: {'ONLINE' if alive else 'OFFLINE'}")
    y -= line_height
    # Codi HTTP retornat
    c.drawString(2 * cm, y, f"Codi d'estat HTTP: {status_code}")
    y -= line_height
    # Temps de càrrega en segons
    c.drawString(2 * cm, y, f"Temps de càrrega: {load_time} segons")

    # Secció de resum tècnic
    y -= 1.2 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Resum tècnic")
    y -= line_height
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, y,
                 "- La puntuació global s'ha calculat a partir de l'estat HTTP i del temps de resposta.")
    y -= line_height
    c.drawString(2 * cm, y,
                 "- Aquest informe es pot ampliar amb més troballes (TLS, certificats, leaks, EoL, etc.).")

    #Una nova pàgina per més evidència
    c.showPage()

    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "Evidència tècnica")

    y = height - 3.5 * cm
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, y, f"URL: {resultat.get('url', '')}")
    y -= line_height
    c.drawString(2 * cm, y, f"alive: {alive}")
    y -= line_height
    c.drawString(2 * cm, y, f"status_code: {status_code}")
    y -= line_height
    c.drawString(2 * cm, y, f"load_time: {load_time}")

    # Guardar el fitxer PDF al disc
    c.save()
