
from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from schema.request_schema import TestInsRequest, TestSelReqeust, TestPutReqeust, TestPatchReqeust, TestDelReqeust 
from core.database import get_db
from services import db_test_service

from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/test")
def insert_test(req: TestInsRequest, db: Session = Depends(get_db)):
    return db_test_service.insert_test(req, db)
        
@router.get("/test")
def select_test(req: TestSelReqeust, db: Session = Depends(get_db)):
    return db_test_service.select_test(req, db)

@router.put("/test")        
def put_test(req: TestPutReqeust, db : Session = Depends(get_db)) :
    return db_test_service.put_test(req, db)
        
@router.patch("/test")        
def patch_test(req: TestPatchReqeust, db : Session = Depends(get_db)) :
    return db_test_service.patch_test(req, db)