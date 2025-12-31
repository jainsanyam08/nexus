def check_github(email: str):
    domain = email.split("@")[-1].lower()

    confidence = 45
    signals = ["GitHub commonly used with this email domain"]

    if domain in ["gmail.com", "outlook.com"]:
        confidence += 5

    if domain not in ["gmail.com", "yahoo.com", "outlook.com"]:
        confidence += 15
        signals.append("Corporate email increases likelihood")

    return {
        "service": "GitHub",
        "confidence": confidence,
        "signals": signals,
        "risk_flags": []
    }
