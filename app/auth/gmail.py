import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_flow():
    client_id = os.getenv("25851036802-trob35np94p0ffmgfs53rpvkt3iqrl7i.apps.googleusercontent.com")
    client_secret = os.getenv("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")

    if not client_id or not client_secret:
        raise RuntimeError("GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET not set")

    return Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [
                    "http://127.0.0.1:8000/auth/gmail/callback"
                ],
            }
        },
        scopes=SCOPES,
    )


def extract_sender_domains(credentials):
    """
    Reads Gmail METADATA ONLY (From headers) and returns sender domains
    """
    service = build("gmail", "v1", credentials=credentials)

    response = service.users().messages().list(
        userId="me",
        maxResults=50
    ).execute()

    domains = set()

    for msg in response.get("messages", []):
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From"]
        ).execute()

        headers = msg_data.get("payload", {}).get("headers", [])
        for h in headers:
            if h["name"] == "From" and "@" in h["value"]:
                domain = h["value"].split("@")[-1].strip(" >").lower()
                domains.add(domain)

    return domains
