from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from app.auth.gmail import get_gmail_flow, extract_sender_domains


from app.deps import get_db
from app.models import Identity, Account, Signal
from app.domain.discovery import discover

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------- LANDING PAGE ----------
@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {"request": request}
    )


# ---------- MAP IDENTITY ----------
@router.post("/identity/map")
def map_identity(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    identity = db.query(Identity).filter_by(email=email).first()
    if not identity:
        identity = Identity(email=email)
        db.add(identity)
        db.commit()
        db.refresh(identity)

    # Clear previous accounts
    db.query(Account).filter_by(identity_id=identity.id).delete()
    db.commit()

    accounts = discover(email)

    for a in accounts:
        acc = Account(
            identity_id=identity.id,
            service=a["service"],
            confidence=a["confidence"]
        )
        db.add(acc)
        db.commit()
        db.refresh(acc)

        for s in a["signals"]:
            db.add(Signal(account_id=acc.id, description=s))

    db.commit()

    return RedirectResponse(
        url=f"/identity/dashboard?email={email}",
        status_code=303
    )

# ---------- CONFIRM / IGNORE ----------
@router.post("/identity/confirm")
async def confirm_account(
    request: Request,
    db: Session = Depends(get_db)
):
    form = await request.form()
    account_id = form.get("account_id")
    email = form.get("email")

    if not account_id or not email:
        return HTMLResponse("Invalid request", status_code=400)

    acc = db.query(Account).filter_by(id=account_id).first()
    if acc:
        acc.confirmed = True
        acc.confidence = min(100, acc.confidence + 20)
        db.commit()

    return RedirectResponse(
        url=f"/identity/dashboard?email={email}",
        status_code=303
    )



@router.post("/identity/ignore")
async def ignore_account(
    request: Request,
    db: Session = Depends(get_db)
):
    form = await request.form()
    account_id = form.get("account_id")
    email = form.get("email")

    if not account_id or not email:
        return HTMLResponse("Invalid request", status_code=400)

    acc = db.query(Account).filter_by(id=account_id).first()
    if acc:
        acc.ignored = True
        db.commit()

    return RedirectResponse(
        url=f"/identity/dashboard?email={email}",
        status_code=303
    )



# ---------- DASHBOARD ----------
@router.get("/identity/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, email: str, db: Session = Depends(get_db)):
    identity = db.query(Identity).filter_by(email=email).first()

    if not identity:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "email": email,
                "accounts": [],
                "score": 100
            }
        )

    accounts = db.query(Account)\
        .filter_by(identity_id=identity.id, ignored=False)\
        .all()

    data = []
    total_penalty = 0

    for acc in accounts:
        signals = db.query(Signal).filter_by(account_id=acc.id).all()
        penalty = 5 + (10 if acc.confidence < 50 else 0)
        total_penalty += penalty

        data.append({
            "id": acc.id,
            "service": acc.service,
            "confidence": acc.confidence,
            "confirmed": acc.confirmed,
            "signals": [s.description for s in signals]
        })

    score = max(20, 100 - total_penalty)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "email": email,
            "accounts": data,
            "score": score
        }
    )

# ---------- GMAIL AUTH ----------
@router.get("/auth/gmail")
def gmail_auth():
    flow = get_gmail_flow()
    flow.redirect_uri = "http://127.0.0.1:8000/auth/gmail/callback"

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return RedirectResponse(auth_url)

@router.get("/auth/gmail/callback")
def gmail_callback(request: Request, db: Session = Depends(get_db)):
    flow = get_gmail_flow()
    flow.redirect_uri = "http://127.0.0.1:8000/auth/gmail/callback"

    # Exchange auth code for tokens
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials

    # Get user's email from ID token
    email = credentials.id_token.get("email")
    if not email:
        return HTMLResponse("Unable to verify Gmail account", status_code=400)

    # Extract sender domains
    domains = extract_sender_domains(credentials)

    identity = db.query(Identity).filter_by(email=email).first()
    if not identity:
        return HTMLResponse("Identity not found", status_code=400)

    accounts = db.query(Account).filter_by(identity_id=identity.id).all()

    for acc in accounts:
        for d in domains:
            if d in acc.service.lower():
                acc.confirmed = True

    db.commit()

    return RedirectResponse(
        url=f"/identity/dashboard?email={email}",
        status_code=303
    )

