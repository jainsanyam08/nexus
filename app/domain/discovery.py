def discover(email: str):
    return [
        {
            "service": "Netflix",
            "confidence": 85,
            "signals": ["Welcome email detected"]
        },
        {
            "service": "LinkedIn",
            "confidence": 75,
            "signals": ["Security alert email detected"]
        },
        {
            "service": "OldForum",
            "confidence": 40,
            "signals": ["Found in public breach dataset"]
        }
    ]
