from datetime import datetime, timedelta

MOCK_ACCOUNTS = [
    ("Netflix", "entertainment", 10),
    ("Spotify", "entertainment", 8),
    ("Dropbox", "storage", 40),
    ("LinkedIn", "social", 20),
    ("OldForum", "other", 85),
]

def discover_accounts():
    now = datetime.utcnow()
    results = []

    for service, category, risk in MOCK_ACCOUNTS:
        results.append({
            "service": service,
            "category": category,
            "risk_score": risk,
            "last_seen_at": now - timedelta(days=risk * 3)
        })

    return results
