import os
import sys
import json
# Asegurar que el root del repo esté en sys.path para que 'backend' sea importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.app.services.model_service import ModelService
from backend.app.models.model_schema import MLModel, CustomProperty
from datetime import datetime


def test_create_model(tmp_path, monkeypatch):
    # Configurar DATA_DIR temporal
    monkeypatch.setenv('DATA_DIR', str(tmp_path))
    svc = ModelService()

    model = MLModel(
        creationTimeStamp=datetime.utcnow(),
        createdBy='tester',
        modifiedTimeStamp=None,
        modifiedBy=None,
        id='',
        name='test-model',
        description='desc',
        scoreCodeType='python',
        algorithm='XGBoost',
        function='classification',
        modeler='tester',
        modelType='python',
        trainCodeType='python',
        targetLevel='ordinal',
        tool='Python',
        toolVersion='3.9',
        externalUrl=None,
        modelVersionName='1.0',
        custom_properties=[]
    )

    res = svc.create_model(model)
    assert res.id != ''
    models_file = tmp_path / 'models.parquet'
    assert models_file.exists()
