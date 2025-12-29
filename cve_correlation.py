import socket
import requests
def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Comprova si hi ha connexió a internet intentant connectar-se a un servidor DNS públic (GOOGLE).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"[!] No hi ha connexió a internet: {ex}")
        return False

def get_cve_Severity(cve):
    """
    Extreu la gravetat d'un CVE donat.
    """
    metrics = cve.get("metrics")
    METRICS = ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2")

    for m in METRICS:
        metric_list = metrics.get(m)
        if not metric_list:
            continue

        metric = metric_list[0]

        if "cvssData" in metric:
            cvss_data = metric["cvssData"]
            return {
                "severity": cvss_data.get("baseSeverity"),
                "score": cvss_data.get("baseScore")
            }
        
        return {
            "severity": metric.get("baseSeverity"),
            "score": metric.get("cvssData", {}).get("baseScore")
        }


def search_cve(list_tech):
    """
    Cerca CVEs per a una llista de tecnologies utilitzant la base de dades local.
    """
    if check_internet():
        cve_results = {}
        for nom, versio in list_tech.items():
            if not versio or versio == '?':
                continue  # Salta tecnologies sense versió coneguda
            else:
                url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
                try:
                    response = requests.get(url,
                                            params={"keywordSearch": f"{nom} {versio}",
                                                    "resultsPerPage": 5},
                                            timeout=10)
                    if response.status_code != 200:
                        print(f"[!] Error en cercar CVEs per {nom} {versio}: Codi d'estat {response.status_code}")
                        continue

                    data = response.json()
                    
                except requests.RequestException as e:
                    print(f"[!] Error en cercar CVEs per {nom} {versio}: {e}")
                    continue

                key = f"{nom} {versio}"
                cve_results[key] = []
                for x in data.get("vulnerabilities"):
                    cve = x.get("cve")
                    cve_id = cve.get("id")
                    if not cve_id:
                        continue

                    cves = get_cve_Severity(cve)
                    cve_results[key].append({
                        "cve": cve_id,
                        "severity": cves.get("severity"),
                        "score": cves.get("score"),
                    })
                if not cve_results[key]:
                    del cve_results[key]  # Elimina entrades sense CVEs trobats
    return cve_results
# llista = {'nginx': '1.19.0', 'php': '5.6.40'}
# print(search_cve(llista))