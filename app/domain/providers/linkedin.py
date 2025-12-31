def check_linkedin(email: str):
    domain = email.split("@")[-1].lower()

    confidence = 50
    signals = ["Email domain frequently used on LinkedIn"]

    if domain not in ["gmail.com", "yahoo.com", "outlook.com"]:
        confidence += 25
        signals.append("Corporate email strongly suggests LinkedIn usage")

    return {
        "service": "LinkedIn",
        "confidence": confidence,
        "signals": signals,
        "risk_flags": [
            "possible_no_2fa"
        ]
    }
