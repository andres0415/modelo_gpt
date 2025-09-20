
from fastapi import APIRouter
from ..services.master import compute_insights

router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('/insights')
def get_insights():
    return compute_insights()
