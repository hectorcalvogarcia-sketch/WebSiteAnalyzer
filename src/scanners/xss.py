import requests
import urllib.parse as urlparse

XSS_PAYLOADS = ["<script>alert(1)</script>","\"><script>alert(1)</script>","<xss>"]

def detect_reflected_xss(url: str) -> list:
    parsed = urlparse.urlparse(url)
    parametros = urlparse.parse_qs(parsed.query)

    vulnerabilidades = []

    if not parametros:
        return vulnerabilidades

    for parametro in parametros:
        for payload in XSS_PAYLOADS:
            injected_parametros = parametros.copy()
            injected_parametros[parametro] = payload

            new_query = urlparse.urlencode(injected_parametros, doseq=True)
            test_url = urlparse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))

            try:
                response = requests.get(test_url, timeout=5)

                if payload in response.text:
                    vulnerabilidades.append({
                        "parametro": parametro,
                        "payload": payload,
                        "url": test_url
                    })

            except requests.exceptions.RequestException:
                continue

    return vulnerabilidades