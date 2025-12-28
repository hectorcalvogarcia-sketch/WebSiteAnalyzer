from datetime import datetime, date


EOL_CATALOG = {
    ("WordPress", "6.0"):  {"support_end": "2024-12-31", "eol": "2025-12-31"},
    ("WordPress", "5.8"):  {"support_end": "2023-12-31", "eol": "2024-12-31"},
    ("Apache", "2.4"):     {"support_end": "2027-01-01", "eol": "2029-01-01"},
    ("Nginx", "1.18"):     {"support_end": "2023-12-31", "eol": "2024-12-31"},
    ("PHP", "7.4"):        {"support_end": "2022-11-28", "eol": "2022-11-28"},
    ("PHP", "8.0"):        {"support_end": "2025-11-26", "eol": "2026-11-26"},
    
}

def _parse_eol_date(s: str | None) -> date | None:
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()

def get_eol_status(product: str, version: str, today: date | None = None) -> dict:
    today = today or date.today()
    key = (product, version)
    info = EOL_CATALOG.get(key)

    if not info:
        return {
            "product": product,
            "version": version,
            "status": "UNKNOWN",
            "support_end": "",
            "eol": "",
        }

    support_end = _parse_eol_date(info.get("support_end"))
    eol = _parse_eol_date(info.get("eol"))

    if eol and eol <= today:
        status = "EOL"
    elif support_end and support_end <= today:
        status = "NO_SUPPORT"
    else:
        status = "SUPPORTED"

    return {
        "product": product,
        "version": version,
        "status": status,
        "support_end": support_end.isoformat() if support_end else "",
        "eol": eol.isoformat() if eol else "",
    }
