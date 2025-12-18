import requests
from datetime import datetime
url = "https://enti.cat/"

def check_certificate_validity(url):
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, stream=True)
    cert = response.raw.connection.sock.getpeercert()
    
    emission_date = cert['notBefore']
    emission_date_formatted = datetime.strptime(emission_date, '%b %d %H:%M:%S %Y %Z')

    expiration_date = cert['notAfter']
    expiration_date_formatted = datetime.strptime(expiration_date, '%b %d %H:%M:%S %Y %Z')
    
    current_date = datetime.utcnow()
    caducity = True if expiration_date_formatted < current_date else False

    print(f"Certificate Emission Date: {emission_date_formatted}")
    print(f"Certificate Expiration Date: {expiration_date_formatted}")

    return caducity

print(check_certificate_validity(url))