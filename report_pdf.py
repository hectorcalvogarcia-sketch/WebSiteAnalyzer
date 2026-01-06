from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def calcular_puntuacio_global(resultat: dict) -> int:
    puntuacio = 100

    # Si la web no està viva, la puntuació és 0 directament
    if not resultat.get("alive", False):
        return 0

    # Penalitzar si el codi d'estat no és 200
    codi = resultat.get("status_code", 0)
    if codi != 200:
        puntuacio -= 20

    # Penalitzar si el temps de càrrega és alt
    temps_carrega = resultat.get("load_time", 0)
    if temps_carrega > 3:
        puntuacio -= 10

    # Limitar la puntuació entre 0 i 100
    return max(0, min(100, puntuacio))


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

    # Calcul i mostra de la puntuació global
    puntuacio = calcular_puntuacio_global(resultat)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 6 * cm, f"Puntuació global: {puntuacio}/100")

    # Passar a una nova pàgina
    c.showPage()

    # === Troballes detallades ===
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

    # Opcional: una nova pàgina per més evidència
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
