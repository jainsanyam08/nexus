def check_spotify(email: str):
    domain = email.split("@")[-1].lower()

    confidence = 40
    signals = ["Consumer email commonly used on Spotify"]

    if domain in ["gmail.com", "outlook.com"]:
        confidence += 15

    return {
        "service": "Spotify",
        "confidence": confidence,
        "signals": signals,
        "risk_flags": []
    }
