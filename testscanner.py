from scanner import analyze_url


def print_results(results: dict):
    print("\n--- RESULTADOS DEL ANÁLISIS ---")
    for key, value in results.items():
        if key == "headers":
            print("\nHeaders HTTP:")
            for h, v in value.items():
                print(f"  {h}: {v}")
        else:
            print(f"{key}: {value}")


def main():
    print("=== WebSec Analyzer - Test Scanner ===")
    url = input("Introduce una URL para analizar: ")

    results = analyze_url(url)

    if "error" in results:
        print("\n❌ Error:", results["error"])
    else:
        print("\n✅ Análisis completado correctamente")
        print_results(results)


if __name__ == "__main__":
    main()