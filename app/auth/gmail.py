from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")


def get_gmail_flow():
    if not os.path.exists(CLIENT_SECRETS_FILE):
        raise RuntimeError("client_secrets.json not found")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/auth/gmail/callback",
    )
    return flow


def extract_sender_domains(credentials):
    service = build("gmail", "v1", credentials=credentials)

    results = service.users().messages().list(
        userId="me",
        maxResults=25
    ).execute()

    domains = set()

    for msg in results.get("messages", []):
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
