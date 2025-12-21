import requests
import time
import urllib.parse as urlparse
import os

def sanitize_url(url: str) -> str:
    return url.strip()


def validate_url(url: str) -> bool:
    parsed = urlparse.urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""

def check_url_alive(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)

        if response.status_code >= 400:
            return {
                "alive": False,
                "error": f"HTTP error {response.status_code}"
            }

        return {
            "alive": True,
            "status_code": response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            "alive": False,
            "error": "Timeout al conectar con el servidor"
        }

    except requests.exceptions.ConnectionError:
        return {
            "alive": False,
            "error": "Error de conexión o DNS"
        }

    except requests.exceptions.RequestException as e:
        return {
            "alive": False,
            "error": str(e)
        }

def measure_load_time(url: str) -> float:
    start = time.time()
    requests.get(url, timeout=5)
    end = time.time()
    return round(end - start, 2)

def get_http_headers(url: str) -> dict:
    response = requests.get(url, timeout=5)
    return dict(response.headers)

def save_scan_status(status: str):
    os.makedirs("data", exist_ok=True)
    with open("data/results.txt", "a") as f:
        f.write(f"Estado escaneo: {status}\n")

def analyze_url(url: str) -> dict:
    url = sanitize_url(url)

    if not validate_url(url):
        return {
            "url": url,
            "error": "URL no válida"
        }

    result = {
        "url": url,
        "https": url.startswith("https")
    }

    alive = check_url_alive(url)

    if not alive["alive"]:
        save_scan_status("FAILED")
        result["alive"] = False
        result["error"] = alive["error"]
        return result

    save_scan_status("RUNNING")

    result["alive"] = True
    result["status_code"] = alive["status_code"]
    result["load_time"] = measure_load_time(url)
    result["headers"] = get_http_headers(url)

    return result
