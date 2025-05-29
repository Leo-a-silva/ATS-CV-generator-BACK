from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.cv import Cv
from ..models.user import User
from ..schemas.cv import CvCreate


def create_cv(db: Session, cv_data: CvCreate) -> Cv:
    # Validate User
    user = db.query(User).filter(User.id == cv_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_cv = Cv(
        first_name=cv_data.first_name,
        last_name=cv_data.last_name,
        email_address=cv_data.email_address,
        phone_number=cv_data.phone_number,
        linkedin_url=cv_data.linkedin_url,
        portfolio_url=cv_data.portfolio_url,
        country=cv_data.country,
        city=cv_data.city,
        summary=cv_data.summary,
        user_id=cv_data.user_id,
    )

    # Saving
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)

    return new_cv
