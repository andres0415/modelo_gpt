
from sqlmodel import Session, select
from ..models import ModelRecord
from ..utils.json_flatten import flatten
from pathlib import Path
import os
import json
import pandas as pd
from datetime import datetime

EXPECTED_CORE = ['name','algorithm','model_type','programming_language']
METRIC_KEYS_CANON = ['accuracy','precision','recall','f1','roc_auc','rmse','mae','mape','bleu','rouge','perplexity']

DATA_DIR = Path(os.getenv('DATA_DIR', Path(__file__).resolve().parents[3] / 'data'))
EXPORT_DIR = DATA_DIR / 'exports'
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _record_to_dict(r: ModelRecord, include_payload: bool = True):
    base = {
        'id': r.id,
        'model_group_id': r.model_group_id,
        'version': r.version,
        'name': r.name,
        'algorithm': r.algorithm,
        'model_type': r.model_type,
        'programming_language': r.programming_language,
        'created_at': r.created_at.isoformat(),
        'updated_at': r.updated_at.isoformat(),
        'is_latest': r.is_latest,
        'source_filename': r.source_filename,
    }
    metrics = {}
    if r.metrics_json:
        try:
            metrics = json.loads(r.metrics_json)
        except Exception:
            metrics = {}
    tags = []
    if r.tags_json:
        try:
            tags = json.loads(r.tags_json)
        except Exception:
            tags = []
    base.update({f'metric.{k}': v for k, v in metrics.items()})
    base['tags'] = ','.join(tags) if tags else None

    if include_payload and r.raw_payload_json:
        try:
            payload = json.loads(r.raw_payload_json)
            flat = {f'payload.{k}': v for k, v in flatten(payload).items()}
            base.update(flat)
        except Exception:
            pass
    return base


def rebuild_master(session: Session):
    """Genera master_all y master_latest en CSV y Parquet."""
    records = session.exec(select(ModelRecord)).all()
    latest = session.exec(select(ModelRecord).where(ModelRecord.is_latest == True)).all()

    all_rows = [_record_to_dict(r) for r in records]
    latest_rows = [_record_to_dict(r) for r in latest]

    if all_rows:
        df_all = pd.DataFrame(all_rows)
        df_all.to_csv(EXPORT_DIR / 'master_all.csv', index=False)
        df_all.to_parquet(EXPORT_DIR / 'master_all.parquet', index=False)
    else:
        # create empty files
        (EXPORT_DIR / 'master_all.csv').write_text('')

    if latest_rows:
        df_latest = pd.DataFrame(latest_rows)
        df_latest.to_csv(EXPORT_DIR / 'master_latest.csv', index=False)
        df_latest.to_parquet(EXPORT_DIR / 'master_latest.parquet', index=False)
    else:
        (EXPORT_DIR / 'master_latest.csv').write_text('')


def compute_insights(session: Session):
    latest = session.exec(select(ModelRecord).where(ModelRecord.is_latest == True)).all()
    total = len(latest)
    por_tipo = {}
    algo_counts = {}
    lang_counts = {}
    metric_keys = set()

    campos_faltantes = []
    metric_values = {k: [] for k in METRIC_KEYS_CANON}

    import json as _json

    for r in latest:
        # tipo
        if r.model_type:
            por_tipo[r.model_type] = por_tipo.get(r.model_type, 0) + 1
        # algoritmo
        if r.algorithm:
            algo_counts[r.algorithm] = algo_counts.get(r.algorithm, 0) + 1
        # lenguaje
        if r.programming_language:
            lang_counts[r.programming_language] = lang_counts.get(r.programming_language, 0) + 1
        # métricas
        metrics = {}
        if r.metrics_json:
            try:
                metrics = _json.loads(r.metrics_json)
            except Exception:
                metrics = {}
        metric_keys.update(metrics.keys())
        for k in METRIC_KEYS_CANON:
            v = metrics.get(k)
            if isinstance(v, (int, float)):
                metric_values[k].append(float(v))
        # campos faltantes
        missing = sum(1 for ck in EXPECTED_CORE if getattr(r, ck if ck!='programming_language' else 'programming_language') in (None, '', []))
        campos_faltantes.append(missing)

    algoritmo_mas_usado = None
    if algo_counts:
        algoritmo_mas_usado = sorted(algo_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
    top_lenguajes = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    promedio_metricas = {k: (sum(v)/len(v) if v else None) for k, v in metric_values.items()}
    campos_faltantes_promedio = (sum(campos_faltantes)/len(campos_faltantes)) if campos_faltantes else 0.0

    return {
        'total_modelos': total,
        'por_tipo': por_tipo,
        'algoritmo_mas_usado': algoritmo_mas_usado,
        'top_lenguajes': [{k: v} for k, v in top_lenguajes],
        'metricas_disponibles': sorted(list(metric_keys)),
        'promedio_metricas': {k: v for k, v in promedio_metricas.items() if v is not None},
        'campos_faltantes_promedio': campos_faltantes_promedio,
    }
