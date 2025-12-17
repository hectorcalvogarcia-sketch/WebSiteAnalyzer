import tkinter as tk
from tkinter import messagebox
from scanner import analyze_url

def scan_url_gui():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Advertencia", "Introduce una URL")
        return
    
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Escaneando...\n")
    
    try:
        result = analyze_url(url)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, str(result))
    except Exception as e:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error inesperado:\n{e}")

root = tk.Tk()
root.title("Escanear URL (Alpha)")
root.geometry("600x400")

tk.Label(root, text="Introduce URL:").pack(pady=10)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

scan_button = tk.Button(root, text="Escanear", command=scan_url_gui)
scan_button.pack(pady=10)

result_text = tk.Text(root, height=15, width=70)
result_text.pack(pady=10)

root.mainloop()
