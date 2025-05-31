from fastapi import APIRouter

from cvs.application.create_cv import CreateCv, CreateCvCommand
from cvs.infrastructure.cv_schema import CvCreate, CvResponse
from cvs.infrastructure.repositories import SQLModelCvsRepository

router = APIRouter()


@router.post("/cvs/", response_model=CvResponse)
def create_cv(payload: CvCreate):
    cv = CreateCv(SQLModelCvsRepository()).execute(
        CreateCvCommand(
            user_id=payload.user_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email_address=payload.email_address,
            phone_number=payload.phone_number,
            linkedin_url=payload.linkedin_url,
            portfolio_url=payload.portfolio_url,
            country=payload.country,
            city=payload.city,
            summary=payload.summary,
        )
    )
    return CvResponse.from_domain(cv)
