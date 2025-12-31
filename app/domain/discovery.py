from app.domain.providers.gravatar import check_gravatar
from app.domain.providers.github import check_github
from app.domain.providers.linkedin import check_linkedin
from app.domain.providers.spotify import check_spotify

def discover(email: str):
    providers = [
        check_gravatar,
        check_github,
        check_linkedin,
        check_spotify
    ]

    results = []

    for provider in providers:
        try:
            res = provider(email)
            if res:
                # clamp confidence
                res["confidence"] = max(20, min(95, res["confidence"]))
                results.append(res)
        except Exception:
            continue

    return results
