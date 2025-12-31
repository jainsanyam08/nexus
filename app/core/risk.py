def explain_risk(account):
    reasons = []

    if account.risk_score > 70:
        reasons.append("High risk due to inactivity")

    if not account.is_verified:
        reasons.append("Account not verified")

    if account.category == "other":
        reasons.append("Unknown service category")

    return reasons
