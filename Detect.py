import requests
import re



def get_response(url: str): 
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    resp = requests.get(url, timeout=10, allow_redirects=True)
    return resp.text, resp.headers, resp.status_code




RULES = [
    
    {
        "name": "WordPress",
        "type": "CMS",
        "where": "html",
        "pattern": r"wp-content|wp-includes",
        "version_regex": r"WordPress\s*([0-9\.]+)",
    },

    
    {
        "name": "Apache",
        "type": "Server",
        "where": "header:Server",
        "pattern": r"Apache",
        "version_regex": r"Apache/?([0-9\.]+)",
    },
    {
        "name": "Nginx",
        "type": "Server",
        "where": "header:Server",
        "pattern": r"nginx",
        "version_regex": r"nginx/?([0-9\.]+)",
    },

    
    {
        "name": "PHP",
        "type": "Backend",
        "where": "header:X-Powered-By",
        "pattern": r"PHP",
        "version_regex": r"PHP/?([0-9\.]+)",
    },
    {
        "name": "ASP.NET",
        "type": "Backend",
        "where": "header:X-Powered-By",
        "pattern": r"ASP\.NET",
        "version_regex": r"ASP\.NET/?([0-9\.]+)",
    },

    
    {
        "name": "jQuery",
        "type": "Frontend",
        "where": "html",
        "pattern": r"jquery(-[0-9\.]+)?\.js",
        "version_regex": r"jquery-([0-9\.]+)\.js",
    },
    {
        "name": "React",
        "type": "Frontend",
        "where": "html",
        "pattern": r"react\.js|react-dom\.js",
        "version_regex": None,
    },
    {
        "name": "Angular",
        "type": "Frontend",
        "where": "html",
        "pattern": r"angular(\.min)?\.js",
        "version_regex": r"angular-([0-9\.]+)\.js",
    },
]




def detect_technologies(url: str):
    html, headers, status = get_response(url)

    
    headers_lower = {k.lower(): v for k, v in headers.items()}

    result = []

    for rule in RULES:
        where = rule["where"]
        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        version_regex = re.compile(rule["version_regex"], re.IGNORECASE) if rule.get("version_regex") else None

        target_text = ""

        if where == "html":
            target_text = html
        elif where.startswith("header:"):
            header_name = where.split(":", 1)[1].lower()
            target_text = headers_lower.get(header_name, "")

        if not target_text:
            continue

        
        if pattern.search(target_text):
            version = None
            if version_regex:
                m = version_regex.search(target_text)
                if m:
                    version = m.group(1)

            result.append({
                "name": rule["name"],
                "type": rule["type"],
                "version": version,
                "source": where,
            })

    return {
        "url": url,
        "status_code": status,
        "technologies": result,
        "headers": dict(headers),
    }




def main():
    url = input("Enter the URL to analyze: ").strip()
    try:
        info = detect_technologies(url)
    except Exception as e:
        print(f"Error while analyzing the URL: {e}")
        return

    print("\n=== Analysis result ===")
    print(f"URL: {info['url']}")
    print(f"HTTP status: {info['status_code']}\n")

    if not info["technologies"]:
        print("No technologies detected with the current rules.")
    else:
        print("Detected technologies:")
        for t in info["technologies"]:
            ver = t["version"] or "unknown"
            print(f"- {t['name']} ({t['type']}), version {ver} [source: {t['source']}]")

   
    print("\nHTTP headers:")
    for k, v in info["headers"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()