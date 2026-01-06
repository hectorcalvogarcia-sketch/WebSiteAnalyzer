def mostrar_seccio(titol, contingut):
    """
    funció auxiliar per formatar i imprimir els resultats a la consola
    """
    print(f"\n{'-'*40}")
    print(f" {titol}")
    print(f"{'-'*40}")
    
    if isinstance(contingut, dict):
        for k, v in contingut.items():
            if isinstance(v, list):
                print(f"{k}:")
                for item in v:
                    print(f"  - {item}")
            elif isinstance(v, dict):
                print(f"{k}:")
                for sub_k, sub_v in v.items():
                    print(f"  - {sub_k}: {sub_v}")
            else:
                print(f"{k}: {v}")
    else:
        print(f"{contingut}")