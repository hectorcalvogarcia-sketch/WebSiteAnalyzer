import requests
import re

# llista de regles per detectar tecnologies com cms o servidors
REGLES = [
    {
        "name": "WordPress",
        "type": "CMS",
        "where": "html",
        "pattern": r"wp-content|wp-includes",
        "version_regex": r"WordPress\s*([0-9\.]+)",
    },
    {
        "name": "Apache",
        "type": "Servidor",
        "where": "header:Server",
        "pattern": r"Apache",
        "version_regex": r"Apache/?([0-9\.]+)",
    },
    {
        "name": "Nginx",
        "type": "Servidor",
        "where": "header:Server",
        "pattern": r"nginx",
        "version_regex": r"nginx/?([0-9\.]+)",
    },
    {
        "name": "PHP",
        "type": "Backend",
        "where": "header:X-Powered-By",
        "pattern": r"PHP",
        "version_regex": r"PHP/?([0-9\.]+)",
    },
    {
        "name": "jQuery",
        "type": "Frontend",
        "where": "html",
        "pattern": r"jquery(-[0-9\.]+)?\.js",
        "version_regex": r"jquery-([0-9\.]+)\.js",
    },
]

def pillar_resposta(url): 
    # descarrega el codi de la web i les capçaleres per analitzar-ho
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return resp.text, resp.headers, resp.status_code
    except:
        # si falla, torna valors buits
        return "", {}, 0

def detect_technologies(url):
    # funció que busca coincidències amb les regles definides a dalt
    html, headers, status = pillar_resposta(url)

    # posa les capçaleres en minúscules per facilitar la cerca
    headers_lower = {k.lower(): v for k, v in headers.items()}

    tecnologies_trobades = []

    for regla in REGLES:
        lloc = regla["where"]
        patro = re.compile(regla["pattern"], re.IGNORECASE)
        regex_versio = re.compile(regla["version_regex"], re.IGNORECASE) if regla.get("version_regex") else None

        text_a_mirar = ""

        # decideix on ha de mirar, si al html o a les capçaleres http
        if lloc == "html":
            text_a_mirar = html
        elif lloc.startswith("header:"):
            nom_header = lloc.split(":", 1)[1].lower()
            text_a_mirar = headers_lower.get(nom_header, "")

        if not text_a_mirar:
            continue

        # si troba el patró, afegeix la tecnologia a la llista
        if patro.search(text_a_mirar):
            versio = None
            # si hi ha regex de versió, prova de trobar-la
            if regex_versio:
                m = regex_versio.search(text_a_mirar)
                if m:
                    versio = m.group(1)

            tecnologies_trobades.append({
                "name": regla["name"],
                "type": regla["type"],
                "version": versio,
            })

    return {
        "url": url,
        "status_code": status,
        "technologies": tecnologies_trobades
    }