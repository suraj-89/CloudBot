from fastapi import Depends
from models import Lead
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Header
from token_verify import verify_token
from fastapi import APIRouter
from models import Lead, LeadCreate ,User
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

router = APIRouter()
security = HTTPBearer()


@router.post("/add-lead")
def add_lead(
    lead: LeadCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        return {"message":"Invalid token"}

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    new_lead = Lead(
        name=lead.name,
        company=lead.company,
        email=lead.email,
        user_id=user.id
    )

    db.add(new_lead)
    db.commit()

    return {"message":"Lead added successfully"}



from fastapi import Depends


@router.get("/leads")
def get_leads(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        return {"message":"Invalid token"}

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    if user.role == "admin":

        leads = db.query(Lead).all()

    else:

        leads = db.query(Lead).filter(
            Lead.user_id == user.id
        ).all()

    return leads

@router.delete("/delete-lead/{lead_id}")
def delete_lead(lead_id: int):

    db = SessionLocal()

    lead = db.query(Lead).filter(
        Lead.id == lead_id
    ).first()

    if not lead:

        return {
            "message": "Lead not found"
        }

    db.delete(lead)

    db.commit()

    return {
        "message": "Lead deleted successfully"
    }


@router.put("/update-lead/{lead_id}")
def update_lead(
    lead_id: int,
    lead_data: LeadCreate
):

    db = SessionLocal()

    lead = db.query(Lead).filter(
        Lead.id == lead_id
    ).first()

    if not lead:

        return {
            "message":"Lead not found"
        }

    lead.name = lead_data.name
    lead.company = lead_data.company
    lead.email = lead_data.email

    db.commit()

    return {
        "message":"Lead updated successfully"
    }