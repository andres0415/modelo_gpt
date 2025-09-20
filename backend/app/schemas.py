
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class ModelBase(BaseModel):
    name: str
    algorithm: Optional[str] = None
    model_type: Optional[str] = Field(default=None, description='supervised|unsupervised|generative')
    programming_language: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    extra_payload: Optional[Dict[str, Any]] = Field(default=None, description='Campos adicionales arbitrarios')

class ModelCreate(ModelBase):
    model_group_id: Optional[str] = None

class ModelEdit(BaseModel):
    # Edición parcial
    name: Optional[str] = None
    algorithm: Optional[str] = None
    model_type: Optional[str] = None
    programming_language: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    extra_payload: Optional[Dict[str, Any]] = None

class ModelOut(ModelBase):
    id: int
    model_group_id: str
    version: int
    created_at: datetime
    updated_at: datetime
    is_latest: bool
    previous_version_id: Optional[int] = None

    class Config:
        from_attributes = True

class InsightOut(BaseModel):
    total_modelos: int
    por_tipo: Dict[str, int]
    algoritmo_mas_usado: Optional[str]
    top_lenguajes: List[Dict[str, int]]
    metricas_disponibles: List[str]
    promedio_metricas: Dict[str, float]
    campos_faltantes_promedio: float
