import hashlib
import requests

def check_gravatar(email: str):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return {
                "service": "Gravatar / WordPress",
                "confidence": 75,
                "signals": [
                    "Public Gravatar image found for this email"
                ],
                "risk_flags": [
                    "public_profile"
                ]
            }
    except Exception:
        pass

    return None
