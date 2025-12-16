import requests
import time
import urllib.parse as urlparse

def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc !=""

def check_url_alive(url: str) -> dict:
    try: 
        response = requests.get(url, timeout=5)
        return { 
            "alive": True, 
            "status_code": response.status_code 
        }
    
    except requests.exceptions.RequestException as e:
        return { 
            "alive": False, 
            "error": str(e) 
        }

def measure_load_time(url:str) -> float:
    start = time.time()
    requests.get(url, timeout=5)
    end = time.time()
    return round(end-start, 2)

def get_http_headleader(url: str) -> dict:
    response = requests.get(url, timeout=5)
    return dict(response.headers)

def analyze_url(url):
    result = { 
        "url": url, 
        "https": url.startswith("https") 
    } 

    alive = check_url_alive(url)
    if not alive["alive"]: 
        result["alive"] = False 
        result["error"] = alive["error"] 
        return result 
    
    result["alive"] = True 
    result["status_code"] = alive["status_code"] 
    result["load_time"] = measure_load_time(url) 
    result["headers"] = get_http_headleader(url) 
    return result 