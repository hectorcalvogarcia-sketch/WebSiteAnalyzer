# WebSec Analyzer

Aquest repositori conté WebSec Analyzer, una eina senzilla i educativa pensada per analitzar la seguretat d’una pàgina web. El projecte inclou el codi necessari per detectar vulnerabilitats bàsiques com Reflected XSS, SQL Injection bàsic i una revisió de capçaleres HTTP relacionades amb la seguretat

### Funcionalitats Principals:

* **Anàlisi de Disponibilitat:** Comprovació de l'estat HTTP i temps de resposta
* **Detecció de Tecnologies:** Identificació del servidor web, backend, i versions
* **Correlació de CVEs:** Cerca de vulnerabilitats conegudes per les versions detectades
* **Auditoria SSL/TLS:** Detecció de certificats caducats, autofirmats o protocols insegurs
* **Anàlisi de Capçaleres:** Revisió de capçaleres de HTTP
* **Escàner SQL Injection:** Proves per detectar SQL Injection
* **Informe PDF:** Generació d'un report amb l'infomació extreta
* **Sistema de Logs:** Registre detallat de l'activitat

## Requisits

Per executar aquest projecte necessites:

* **Llenguatge:** [Python 3.8](https://www.python.org/downloads/) o superior.
* **Connexió a Internet:** Necessària per consultar bases de dades de CVE i escanejar l'objectiu.

### Dependències Externes

El projecte utilitza les seguents llibreries externes:

* `requests`: Per les peticions HTTP
* `reportlab`: Per la generació del PDF

---

## Instal·lació

Segueix aquests passos per preparar l'entorn de desenvolupament:

1. **Clonar el repositori:**

   ```bash
   git clone [https://github.com/hectorcalvogarcia-sketch/WebSec-Analyzer](https://github.com/hectorcalvogarcia-sketch/WebSec-Analyzer)
   cd WebSec-Analyzer
   ```
2. **Opcional (Recomanat): Crear un entorn virtual:**

   ```bash
   python -m venv venv
   # A Windows:
   venv\Scripts\activate
   # A Linux/Mac:
   source venv/bin/activate
   ```
3. **Instal·lar les dependències:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Instruccions d'Ús

### Execució

Per arrencar l'aplicació, executa el fitxer principal des de l'arrel del projecte:

```bash
python main.py
```
