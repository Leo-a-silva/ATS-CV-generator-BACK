from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.cv import CvResponse, CvCreate
from ..crud.create_cv import create_cv as create_cv_crud

router = APIRouter()


@router.post("/create-cv/", response_model=CvResponse, status_code=201)
def create_cv(cv_data: CvCreate, db: Session = Depends(get_db)):
    return create_cv_crud(db=db, cv_data=cv_data)
