from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CustomProperty(BaseModel):
    name: str
    value: str
    type: str

class MLModel(BaseModel):
    creationTimeStamp: datetime
    createdBy: str
    modifiedTimeStamp: Optional[datetime]
    modifiedBy: Optional[str]
    id: str
    name: str
    description: str
    scoreCodeType: str
    algorithm: str
    function: str
    modeler: str
    modelType: str
    trainCodeType: str
    targetLevel: str
    tool: str
    toolVersion: str
    externalUrl: Optional[str]
    modelVersionName: str
    custom_properties: List[CustomProperty]
    version: int = 1  # Para manejar el versionamiento

    class Config:
        json_schema_extra = {
            "example": {
                "creationTimeStamp": "2025-03-12T16:50:51.979Z",
                "createdBy": "Andres.Acevedo",
                "id": "8469c4b4-0960-4149-89e3-2b72f0da2666",
                "name": "BAC_VALOR-CLIENTE-CRI-HIP-12M_PRED_XGB_M",
                "description": "Modelo de predicción...",
                "scoreCodeType": "python",
                "algorithm": "XGBoost",
                "function": "classification",
                "modeler": "andres.acevedo",
                "modelType": "python",
                "trainCodeType": "python",
                "targetLevel": "ordinal",
                "tool": "Python 3",
                "toolVersion": "3.9",
                "modelVersionName": "1.0",
                "custom_properties": []
            }
        }