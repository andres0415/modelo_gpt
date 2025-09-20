from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Optional
import json
from datetime import datetime
import uuid
from pathlib import Path

from ..models.model_schema import MLModel
from ..services.model_service import ModelService

router = APIRouter(prefix='/models', tags=['models'])
model_service = ModelService()

@router.post('', response_model=MLModel)
def register_model(model: MLModel):
    return model_service.create_model(model)

@router.post('/from-json-file', response_model=MLModel)
async def register_from_json_file(file: UploadFile = File(...)):
    print(f"Recibiendo archivo: {file.filename}")
    if not file.filename.lower().endswith('.json'):
        raise HTTPException(status_code=400, detail='El archivo debe ser .json')
    
    try:
        content = await file.read()
        print("Contenido del archivo recibido")
        data = json.loads(content)
        print("JSON parseado correctamente")
        print(f"Datos recibidos: {json.dumps(data, indent=2)}")
        
        # Asegurarse de que custom_properties sea una lista
        if "custom_properties" in data and not isinstance(data["custom_properties"], list):
            data["custom_properties"] = []
        
        model = MLModel(**data)
        print("Modelo creado desde JSON")
        result = model_service.create_model(model)
        print(f"Modelo guardado con ID: {result.id}")
        return result
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {str(e)}")
        raise HTTPException(status_code=400, detail=f'JSON inválido: {str(e)}')
    except Exception as e:
        print(f"Error procesando modelo: {str(e)}")
        raise HTTPException(status_code=400, detail=f'Error procesando modelo: {str(e)}')

@router.get("/{model_id}", response_model=MLModel)
async def get_model(model_id: str, version: Optional[int] = None):
    model = model_service.get_model(model_id, version)
    if not model:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    return model

@router.put("/{model_id}", response_model=MLModel)
async def update_model(model_id: str, model: MLModel):
    updated_model = model_service.update_model(model_id, model)
    if not updated_model:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    return updated_model

@router.get("/", response_model=List[MLModel])
async def get_all_models(latest_only: bool = True):
    return model_service.get_all_models(latest_only)

@router.get("/summary/dashboard/")
async def get_models_summary():
    return model_service.get_models_summary()