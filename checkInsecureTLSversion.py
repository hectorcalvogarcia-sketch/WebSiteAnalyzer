import requests

url = "https://enti.cat/"

def insecure_tls_version(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, stream=True)
    tls_Version = response.raw.connection.sock.version()
    insecure_TLS_versions = ['TLSv1.0', 'TLSv1.1']
    return True if tls_Version in insecure_TLS_versions else False

print(insecure_tls_version(url))