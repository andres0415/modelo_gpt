import uuid


import pandas as pd
from pathlib import Path
import os, json

DATA_DIR = Path(os.getenv('DATA_DIR', Path(__file__).resolve().parents[2] / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)
PARQUET_PATH = DATA_DIR / 'models.parquet'
CSV_PATH = DATA_DIR / 'models.csv'

MODEL_COLUMNS = [
    'id', 'model_group_id', 'version', 'name', 'algorithm', 'model_type', 'programming_language',
    'metrics_json', 'tags_json', 'raw_payload_json', 'source_filename',
    'created_at', 'updated_at', 'is_latest', 'previous_version_id'
]

def _init_files():
    if not PARQUET_PATH.exists() or not CSV_PATH.exists():
        df = pd.DataFrame(columns=MODEL_COLUMNS)
        df.to_parquet(PARQUET_PATH, index=False)
        df.to_csv(CSV_PATH, index=False)

def read_models():
    if PARQUET_PATH.exists():
        return pd.read_parquet(PARQUET_PATH)
    else:
        return pd.DataFrame(columns=MODEL_COLUMNS)

def save_models(df):
    df.to_parquet(PARQUET_PATH, index=False)
    df.to_csv(CSV_PATH, index=False)

def add_model(record: dict):
    df = read_models()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    save_models(df)

def update_model(model_id, updates: dict):
    df = read_models()
    mask = df['id'] == model_id
    for key, value in updates.items():
        df.loc[mask, key] = value
    save_models(df)

def delete_model(model_id):
    df = read_models()
    df = df[df['id'] != model_id]
    save_models(df)

def get_model(model_id):
    df = read_models()
    result = df[df['id'] == model_id]
    if not result.empty:
        return result.iloc[0].to_dict()
    return None

def init_db():
    _init_files()
