try:
    from src.gui import gui
except ImportError:
    print("Error important la interfície gràfica. Assegura't que tots els fitxers estan al directori correcte.")
    
if __name__ == "__main__":
    #iniciem la interfície gràfica
    print("Iniciant la interfície gràfica...")
    gui.launch()