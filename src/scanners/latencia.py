import requests
import time

def measure_response_time(url: str) -> dict:
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()

        response_time = round(end_time - start_time, 2)

        if response_time < 1:
            rendimiento = "BUENO"
        elif response_time < 3:
            rendimiento = "ACEPTABLE"
        else:
            rendimiento = "LENTO"

        return {
            "response_time": response_time,
            "performance": rendimiento,
            "status_code": response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Timeout al medir el tiempo de respuesta"
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }