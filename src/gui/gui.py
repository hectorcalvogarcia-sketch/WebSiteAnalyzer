import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import src.gui.gui_functions as logic

root = None
entrada = None
pantalla = None
boto = None
boto_guardar = None


def bot_click():
    url = entrada.get()
    if not url:
        messagebox.showwarning("Error", "Posa una URL!")
        return
    
    # Netegem pantalla
    pantalla.config(state=tk.NORMAL)
    pantalla.delete(1.0, tk.END)
    pantalla.config(state=tk.DISABLED)
    
    # Desactivem botons mentre treballa
    boto.config(state=tk.DISABLED)
    boto_guardar.config(state=tk.DISABLED) # <--- També desactivem el de guardar
    boto.update()
    
    # Cridem a la lògica (es quedarà aquí fins que acabi)
    logic.executar_escaner(url, pantalla)
    
    # Reactivem botons
    boto.config(state=tk.NORMAL)
    boto_guardar.config(state=tk.NORMAL) # <--- Ara ja podem guardar

# # --- 2. NOVA FUNCIÓ PER GUARDAR ---
# def guardar_txt():
#     # Aquesta funció agafa tot el text de la pantalla i el posa en un fitxer
    
#     # Obrim la finestra de "Guardar com..."
#     fitxer = filedialog.asksaveasfilename(
#         defaultextension=".txt",
#         filetypes=[("Fitxers de text", "*.txt"), ("Tots els fitxers", "*.*")],
#         title="Guardar Informe de Seguretat"
#     )
    
#     # Si l'usuari no ha cancel·lat (ha triat un fitxer)
#     if fitxer:
#         try:
#             # Llegim el text de la pantalla: des de la línia 1, caràcter 0 ("1.0") fins al final (tk.END)
#             contingut = pantalla.get("1.0", tk.END)
            
#             # Escrivim al fitxer
#             with open(fitxer, "w", encoding="utf-8") as f:
#                 f.write(contingut)
            
#             messagebox.showinfo("Èxit", "Informe guardat correctament!")
#         except Exception as e:
#             messagebox.showerror("Error", f"No s'ha pogut guardar: {e}")

def guardar_pdf():
    """
    Esta función abre la ventana de 'Guardar como'.
    ESTA es la función que debe llamar el botón, no la de 'logic'.
    """
    fitxer = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Document", "*.pdf")],
        title="Guardar Informe PDF"
    )
    
    if fitxer:
        # Una vez tenemos el nombre del archivo, AHORA SÍ llamamos a la lógica
        ok, missatge = logic.generar_pdf_logic(fitxer)
        
        if ok:
            messagebox.showinfo("Èxit", missatge)
        else:
            messagebox.showerror("Error", missatge)


def launch():
    # --- CONFIGURACIÓ DE LA FINESTRA ---
    global root, entrada, pantalla, boto, boto_guardar
    root = tk.Tk()
    root.title("WebSec Analyzer")
    root.geometry("750x650") # Una mica més alt per encabir el botó nou

    tk.Label(root, text="URL a analitzar:").pack(pady=10)

    entrada = tk.Entry(root, width=50)
    entrada.pack(pady=5)

    # Frame (contenidor) per posar els botons un al costat de l'altre
    frame_botons = tk.Frame(root)
    frame_botons.pack(pady=10)

    boto = tk.Button(frame_botons, text="Començar Anàlisi", command=bot_click, bg="#dddddd")
    boto.pack(side=tk.LEFT, padx=10)

    # --- 3. EL NOU BOTÓ DE GUARDAR ---
    boto_guardar = tk.Button(frame_botons, text="Guardar Resultats", command=guardar_pdf, bg="#ccffcc")
    boto_guardar.pack(side=tk.LEFT, padx=10)

    pantalla = scrolledtext.ScrolledText(root, width=77, height=32)
    pantalla.pack(padx=10, pady=10)
    pantalla.config(state=tk.DISABLED)

    root.mainloop()