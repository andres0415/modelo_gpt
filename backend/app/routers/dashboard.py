
# from fastapi import APIRouter
# from sqlmodel import Session
# from ..database import get_session
from ..services.master import compute_insights

router = APIRouter(prefix='/dashboard', tags=['dashboard'])

@router.get('/insights')
    return compute_insights()
