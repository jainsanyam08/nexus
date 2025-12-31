def calculate_identity_score(accounts):
    if not accounts:
        return 100

    avg_risk = sum(a.risk_score for a in accounts) / len(accounts)
    return max(0, 100 - int(avg_risk))
