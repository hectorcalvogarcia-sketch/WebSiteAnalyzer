import requests
import time
import urllib.parse as urlparse

def validar_url(url):
    # mira si l'url és vàlida a priori i comença per http o https
    parsed = urlparse.urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""

def mirar_si_respon(url):
    # prova de connectar 
    try:
        response = requests.get(url, timeout=5)
        # torna un diccionari dient que està alive i el codi d'estat
        return {"alive": True, "status_code": response.status_code}
    except Exception as e:
        # si falla torna que no està alive i l'error
        return {"alive": False, "error": str(e)}

def mesurar_temps(url):
    # cronometra quant triga a carregar la pàgina
    start = time.time()
    try:
        requests.get(url, timeout=5)
    except:
        pass
    end = time.time()
    # arrodoneix a 2 decimals per sanititzar
    return round(end - start, 2)

def analyze_url(url):
    # funció principal per analitzar l'url
    url = url.strip()

    if not validar_url(url):
        return {"url": url, "error": "url no vàlida", "alive": False}

    resultat = {"url": url}

    # mira si respon
    estat = mirar_si_respon(url)
    if not estat["alive"]:
        resultat["alive"] = False
        resultat["error"] = estat["error"]
        return resultat

    # si arriba a aquí és que està online
    resultat["alive"] = True
    resultat["status_code"] = estat["status_code"]
    resultat["load_time"] = mesurar_temps(url)

    return resultat