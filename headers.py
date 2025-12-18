import requests # librería para conectar con servidores y descargar páginas web
import re # librería para buscar patrones de texto específicos (como el título) dentro del código

# pedir URL al usuario
url = input("Introduce URL (ej: google.com): ")

# "autocorrector": asegurar que empieza por https://
if not url.startswith("http"):
    url = "https://" + url

# definir cabeceras para parecer un navegador real y evitar bloqueos (403 Forbidden)
cabeceras_navegador = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Conectando a {url}...")

try:
    # hacer la petición enviando nuestras cabeceras falsas
    respuesta = requests.get(url, headers=cabeceras_navegador, timeout=10, allow_redirects=True)
    
    # mostrar estado, latencia y codificación
    print("\n--- ESTADO DE LA CONEXIÓN ---")
    print(f"Estado final de la solicitud: {respuesta.status_code} ({respuesta.reason})")
    print(f"Latencia (tiempo de respuesta): {respuesta.elapsed.total_seconds()} segundos")
    print(f"Codificación detectada: {respuesta.encoding}")

    # comprobar si hubo redirecciones
    if respuesta.history:
        print("\n--- RASTREO DE REDIRECCIONES ---")
        for paso in respuesta.history:
            print(f"Redirigido desde '{paso.url}' a '{respuesta.url}' (Estado: {paso.status_code})")

    # analizar el contenido HTML descargado (peso y título)
    print("\n--- ANÁLISIS DE CONTENIDO ---")
    peso_kb = len(respuesta.content) / 1024
    print(f"Peso de la respuesta: {peso_kb:.2f} KB")

    # buscar el título de la página usando una expresión regular simple
    titulo = re.findall('<title>(.*?)</title>', respuesta.text, re.IGNORECASE)
    if titulo:
        print(f"Título de la web: {titulo[0].strip()}")
    else:
        print("Título de la web: No encontrado")

    # buscar cabeceras de seguridad específicas
    print("\n--- CHECK DE SEGURIDAD ---")
    claves_seguridad = ['Strict-Transport-Security', 'X-Frame-Options', 'Content-Security-Policy', 'Server', 'X-Powered-By']
    
    for clave in claves_seguridad:
        valor = respuesta.headers.get(clave, "NO PRESENTE ⚠️")
        print(f"{clave}: {valor}")

    # mostrar cookies con detalles de seguridad
    print("\n--- COOKIES DETECTADAS ---")
    if not respuesta.cookies:
        print("No se detectaron cookies en la respuesta inicial.")
    else:
        for cookie in respuesta.cookies:
            seguridad = "✅ Segura" if cookie.secure else "❌ No segura"
            print(f"Nombre: {cookie.name} | Seguridad: {seguridad} | Dominio: {cookie.domain}")

except requests.exceptions.Timeout:
    print("❌ Error: Tiempo de espera agotado (Timeout).") # error si se agota el tiempo de espera

except requests.exceptions.ConnectionError:
    print("❌ Error: Problema de conexión (DNS o Red).") # error si falla la conexión o DNS

except Exception as e:
    print(f"❌ Ocurrió un error: {e}") # si algo falla inesperadamente


