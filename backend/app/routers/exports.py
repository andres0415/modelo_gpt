
from fastapi import APIRouter
# from sqlmodel import Session
# from ..database import get_session
from ..services.master import rebuild_master

router = APIRouter(prefix='/exports', tags=['exports'])

@router.post('/rebuild')
def rebuild():
    rebuild_master()
    return {'status':'ok'}
