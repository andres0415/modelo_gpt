import pandas as pd
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..models.model_schema import MLModel, CustomProperty
import os

class ModelService:
    def __init__(self):
        self.data_dir = Path(os.getenv('DATA_DIR', Path(__file__).resolve().parents[3] / 'data'))
        self.models_file = self.data_dir / 'models.parquet'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.df = self._load_or_create_df()

    def _load_or_create_df(self) -> pd.DataFrame:
        if self.models_file.exists():
            print(f"Cargando datos desde: {self.models_file}")
            return pd.read_parquet(self.models_file)
        print("No se encontró archivo de datos, creando uno nuevo")
        return pd.DataFrame()

    def _save_df(self):
        print(f"Guardando datos en: {self.models_file}")
        self.df.to_parquet(self.models_file, index=False)
        try:
            # Regenerar exports después de guardar
            from .master import rebuild_master
            print("Regenerando exports master...")
            rebuild_master()
        except Exception as e:
            print(f"Warning: fallo al regenerar exports: {e}")

    def create_model(self, model: MLModel) -> MLModel:
        try:
            print("Iniciando creación del modelo")
            if not model.id:
                model.id = str(uuid.uuid4())
                print(f"Generado nuevo ID: {model.id}")
            
            print("Convirtiendo modelo a diccionario")
            # Usar .dict() para compatibilidad con pydantic v1
            if hasattr(model, 'dict'):
                model_dict = model.dict()
            else:
                # pydantic v2 fallback
                model_dict = model.model_dump()
            
            print("Procesando propiedades personalizadas")
            if hasattr(model, 'custom_properties'):
                model_dict["custom_properties"] = [
                    (prop.dict() if hasattr(prop, 'dict') else prop.model_dump()) if hasattr(prop, 'model_dump') or hasattr(prop, 'dict') else prop
                    for prop in model.custom_properties
                ]
            
            print("Creando DataFrame con los datos del modelo")
            new_row = pd.DataFrame([model_dict])
            print(f"Columnas en el nuevo DataFrame: {new_row.columns.tolist()}")
            
            if self.df.empty:
                print("DataFrame vacío, iniciando nuevo DataFrame")
                self.df = new_row
            else:
                print("Concatenando con DataFrame existente")
                print(f"Columnas existentes: {self.df.columns.tolist()}")
                self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            print("Guardando cambios")
            self._save_df()
            print(f"Modelo guardado exitosamente con ID: {model.id}")
            
            return model
        except Exception as e:
            print(f"Error en create_model: {str(e)}")
            raise

    def update_model(self, model_id: str, model: MLModel) -> Optional[MLModel]:
        if not self.df.empty and model_id in self.df["id"].values:
            # Incrementar versión y actualizar timestamps
            current_version = self.df[self.df["id"] == model_id]["version"].max()
            model.version = current_version + 1
            model.modifiedTimeStamp = datetime.now()
            
            if hasattr(model, 'dict'):
                model_dict = model.dict()
            else:
                model_dict = model.model_dump()
            model_dict["custom_properties"] = [prop.dict() if hasattr(prop, 'dict') else prop.model_dump() for prop in model.custom_properties]
            
            self.df = pd.concat([self.df, pd.DataFrame([model_dict])], ignore_index=True)
            self._save_df()
            return model
        return None

    def get_model(self, model_id: str, version: Optional[int] = None) -> Optional[MLModel]:
        if self.df.empty or model_id not in self.df["id"].values:
            return None
        
        model_df = self.df[self.df["id"] == model_id]
        if version:
            model_df = model_df[model_df["version"] == version]
        else:
            # Obtener la última versión
            max_version = model_df["version"].max()
            model_df = model_df[model_df["version"] == max_version]
        
        if model_df.empty:
            return None
            
        model_data = model_df.iloc[0].to_dict()
        model_data["custom_properties"] = [
            CustomProperty(**prop) for prop in model_data["custom_properties"]
        ]
        return MLModel(**model_data)

    def get_models_summary(self) -> dict:
        if self.df.empty:
            return {}
        
        latest_versions = self.df.sort_values("version").groupby("id").last()
        
        return {
            "total_models": len(latest_versions),
            "algorithms": latest_versions["algorithm"].value_counts().to_dict(),
            "functions": latest_versions["function"].value_counts().to_dict(),
            "languages": latest_versions["scoreCodeType"].value_counts().to_dict(),
            "model_types": latest_versions["modelType"].value_counts().to_dict(),
            "target_levels": latest_versions["targetLevel"].value_counts().to_dict(),
            "tools": latest_versions["tool"].value_counts().to_dict(),
        }

    def get_all_models(self, latest_only: bool = True) -> List[MLModel]:
        if self.df.empty:
            return []
            
        if latest_only:
            models_df = self.df.sort_values("version").groupby("id").last()
        else:
            models_df = self.df
            
        models = []
        for _, row in models_df.iterrows():
            model_data = row.to_dict()
            model_data["custom_properties"] = [
                CustomProperty(**prop) for prop in model_data["custom_properties"]
            ]
            models.append(MLModel(**model_data))
            
        return models