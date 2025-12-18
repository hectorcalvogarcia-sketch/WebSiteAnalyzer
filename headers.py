import requests

# pedir URL al usuario
url = input("Introduce URL (ej: google.com): ")

# "autocorrector": asegurar que empieza por https://
if not url.startswith("http"):
    url = "https://" + url

print(f"Conectando a {url}...")

try:
    # hacer la petición permitiendo redirecciones automáticas
    respuesta = requests.get(url, timeout=5, allow_redirects=True)
    
    # mostrar estado y latencia de la respuesta
    print("\n--- ESTADO DE LA CONEXIÓN ---")
    print(f"Código Final: {respuesta.status_code} ({respuesta.reason})")
    print(f"Latencia: {respuesta.elapsed.total_seconds()} segundos")

    # comprobar si hubo redirecciones antes de llegar a la URL final
    if respuesta.history:
        print("\n--- RASTREO DE REDIRECCIONES ---")
        for paso in respuesta.history:
            print(f"Saltó desde {paso.url} a {respuesta.url} (Estado: {paso.status_code})")

    # buscar cabeceras de seguridad específicas
    print("\n--- CHECK DE SEGURIDAD ---")
    claves_seguridad = ['Strict-Transport-Security', 'X-Frame-Options', 'Content-Security-Policy', 'Server']
    
    for clave in claves_seguridad:
        valor = respuesta.headers.get(clave, "NO PRESENTE ⚠️") # obtener el valor o avisar si no está presente
        print(f"{clave}: {valor}")

    # mostrar cookies con detalles de seguridad
    print("\n--- COOKIES DETECTADAS ---")
    if not respuesta.cookies:
        print("No se detectaron cookies en la respuesta inicial.")
    else:
        for cookie in respuesta.cookies:
            print(f"Nombre: {cookie.name} | Seguridad: {cookie.secure} | Dominio: {cookie.domain}") # mostrar nombre, seguridad y dominio

except requests.exceptions.Timeout:
    print("❌ Error: Tiempo de espera agotado (Timeout).") # error si se agota el tiempo de espera

except requests.exceptions.ConnectionError:
    print("❌ Error: Problema de conexión (DNS o Red).") # error si falla la conexión o DNS

except Exception as e:
    print(f"❌ Ocurrió un error: {e}") # si algo falla inesperadamente