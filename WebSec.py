import requests
from datetime import datetime
url = "https://enti.cat/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, stream=True)
cert = response.raw.connection.sock.getpeercert()

emission_date = cert['notBefore']
expiration_date = cert['notAfter']

emission_date_formatted = datetime.strptime(emission_date, '%b %d %H:%M:%S %Y %Z')
expiration_date_formatted = datetime.strptime(expiration_date, '%b %d %H:%M:%S %Y %Z')

print(f"Certificate Emission Date: {emission_date_formatted}")
print(f"Certificate Expiration Date: {expiration_date_formatted}")