
from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ModelRecord(SQLModel, table=True):
    __tablename__ = 'model_records'
    id: Optional[int] = Field(default=None, primary_key=True)
    # Agrupador para versionamiento
    model_group_id: str = Field(index=True, default_factory=lambda: str(uuid.uuid4()))
    version: int = Field(default=1, index=True)

    name: str = Field(index=True)
    algorithm: Optional[str] = Field(default=None, index=True)
    model_type: Optional[str] = Field(default=None, index=True, description='supervised|unsupervised|generative')
    programming_language: Optional[str] = Field(default=None, index=True)

    metrics_json: Optional[str] = Field(default=None, description='JSON str con métricas')
    tags_json: Optional[str] = Field(default=None, description='JSON str con lista de tags')
    raw_payload_json: Optional[str] = Field(default=None, description='JSON str con el objeto completo original')

    source_filename: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    is_latest: bool = Field(default=True, index=True)
    previous_version_id: Optional[int] = Field(default=None, foreign_key='model_records.id')
