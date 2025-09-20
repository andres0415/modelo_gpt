
from sqlmodel import Session
from app.database import engine
from app.routers.models import bulk_ingest

if __name__ == '__main__':
    with Session(engine) as session:
        print('Ingestas realizadas:', len(bulk_ingest.__wrapped__(session=session)))
