import requests

# pedir URL al usuario
url = input("Introduce URL (ej: google.com): ")

# "autocorrector": asegurar que empieza por https://
if not url.startswith("http"):
    url = "https://" + url

print(f"Conectando a {url}...")

try:
    # hacer la petición con timeout de 5 segundos que evita que el programa se cuelgue si la web no responde
    respuesta = requests.get(url, timeout=5)
    
    # mostrar cabeceras 
    print("\n--- CABECERAS DEL SERVIDOR (Raw Data) ---")
    for nombre, valor in respuesta.headers.items():
        print(f"{nombre}: {valor}")

    # mostrar cookies 
    print("\n--- COOKIES DETECTADAS ---")
    if not respuesta.cookies:
        print("No se detectaron cookies en la respuesta inicial.")
    else:
        for cookie in respuesta.cookies:
            # mostrar Nombre y si tiene el candado (Secure)
            print(f"Nombre: {cookie.name} | ¿Es Segura?: {cookie.secure}")

except Exception as e:
    # si algo falla (no hay internet, web caída), mostrar aquí
    print(f"❌ Ocurrió un error: {e}")