import requests
import re

def analitzar_capcaleres(url): # analitza la informació bàsica i les capçaleres del web
    resultats = {}
    # fa veure que és un navegador normal per evitar bloquejos
    capcaleres_navegador = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # connecta al web i espera un màxim de 10 segons
        resp = requests.get(url, headers=capcaleres_navegador, timeout=10, allow_redirects=True)
        
        # desa les dades bàsiques de la resposta
        resultats['Codi Estat'] = resp.status_code
        resultats['Codificació'] = resp.encoding
        # mira si ens han redirigit a una altra adreça
        resultats['Redireccions'] = [r.url for r in resp.history]
        # calcula quant pesa la pàgina en kilobytes
        resultats['Pes (KB)'] = round(len(resp.content) / 1024, 2)
        # cerca el títol de la pàgina dins del codi
        titol = re.findall('<title>(.*?)</title>', resp.text, re.IGNORECASE)
        resultats['Títol web'] = titol[0].strip() if titol else "no té títol"
        # comprova si estan actives les mesures de seguretat típiques
        capcaleres_seguretat = ['Strict-Transport-Security', 'X-Frame-Options', 'Content-Security-Policy', 'Server', 'X-Powered-By']
        resultats['Capçaleres'] = {k: resp.headers.get(k, "no existeix") for k in capcaleres_seguretat}
        
        # desa les cookies i mira si són segures
        resultats['Cookies'] = []
        for cookie in resp.cookies:
            resultats['Cookies'].append(f"{cookie.name} (segura: {cookie.secure})")
            
    except Exception as e:
        # si alguna cosa falla desa l'error
        resultats['ERROR'] = str(e)
        
    return resultats