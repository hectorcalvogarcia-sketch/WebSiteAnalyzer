import requests
from urllib.parse import urljoin

sensitive_files = [
    ".env",
    "config.php",
    "config.json",
    "config.yml",
    "backup.zip",
    "backup.tar.gz",
    "db.sql",
    "database.sql",
    "admin.bak",
    "index.bak",
    "wp-config.php",
    ".git/config"
]


def file_hunter(url: str) -> list:
    found_files = []

    for file_path in sensitive_files:
        target_url = urljoin(url + "/", file_path)

        try:
            response = requests.get(target_url, timeout=5)

            if response.status_code == 200:
                found_files.append({
                    "file": file_path,
                    "url": target_url,
                    "status": "EXPOSED",
                    "http_code": response.status_code
                })

            elif response.status_code in (401, 403):
                found_files.append({
                    "file": file_path,
                    "url": target_url,
                    "status": "PROTECTED",
                    "http_code": response.status_code
                })

        except requests.exceptions.RequestException:
            continue

    return found_files
