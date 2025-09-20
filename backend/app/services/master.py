
from pathlib import Path
import os
import json
import pandas as pd
from ..utils.json_flatten import flatten

METRIC_KEYS_CANON = ['accuracy','precision','recall','f1','roc_auc','rmse','mae','mape','bleu','rouge','perplexity']

DATA_DIR = Path(os.getenv('DATA_DIR', Path(__file__).resolve().parents[3] / 'data'))
MODELS_FILE = DATA_DIR / 'models.parquet'
EXPORT_DIR = DATA_DIR / 'exports'
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_row(row: dict, include_payload: bool = True):
    base = {}
    # Campos básicos
    base['id'] = row.get('id')
    base['version'] = row.get('version')
    base['name'] = row.get('name')
    base['algorithm'] = row.get('algorithm')
    base['model_type'] = row.get('modelType') or row.get('model_type')
    base['programming_language'] = row.get('scoreCodeType') or row.get('programming_language')
    base['created_at'] = row.get('creationTimeStamp')
    base['updated_at'] = row.get('modifiedTimeStamp')
    base['is_latest'] = True
    # metrics and tags if present inside payload
    metrics = {}
    payload = row.get('raw_payload') or row.get('raw_payload_json') or row
    # Try to extract metrics field
    if isinstance(payload, dict):
        metrics = payload.get('metrics', {}) if payload.get('metrics') else {}

    base.update({f'metric.{k}': v for k, v in (metrics or {}).items()})

    # Flatten raw payload
    if include_payload and isinstance(payload, dict):
        flat = {f'payload.{k}': v for k, v in flatten(payload).items()}
        base.update(flat)

    return base


def rebuild_master():
    """Lee data/models.parquet y genera exports/master_all(.csv|.parquet) y master_latest."""
    if not MODELS_FILE.exists():
        # crear archivos vacíos
        (EXPORT_DIR / 'master_all.csv').write_text('')
        (EXPORT_DIR / 'master_latest.csv').write_text('')
        return

    df = pd.read_parquet(MODELS_FILE)
    if df.empty:
        (EXPORT_DIR / 'master_all.csv').write_text('')
        (EXPORT_DIR / 'master_latest.csv').write_text('')
        return

    # master_all
    all_rows = [ _normalize_row(r) for r in df.to_dict(orient='records') ]
    df_all = pd.DataFrame(all_rows)
    df_all.to_csv(EXPORT_DIR / 'master_all.csv', index=False)
    df_all.to_parquet(EXPORT_DIR / 'master_all.parquet', index=False)

    # master_latest: agrupar por id y tomar la última versión
    if 'id' in df.columns and 'version' in df.columns:
        latest_df = df.sort_values('version').groupby('id', as_index=False).last()
    else:
        latest_df = df

    latest_rows = [ _normalize_row(r) for r in latest_df.to_dict(orient='records') ]
    df_latest = pd.DataFrame(latest_rows)
    df_latest.to_csv(EXPORT_DIR / 'master_latest.csv', index=False)
    df_latest.to_parquet(EXPORT_DIR / 'master_latest.parquet', index=False)


def compute_insights():
    """Calcula insights a partir de exports/master_latest.parquet (si existe) o del models.parquet."""
    latest_file = EXPORT_DIR / 'master_latest.parquet'
    if latest_file.exists():
        df = pd.read_parquet(latest_file)
    elif MODELS_FILE.exists():
        df_raw = pd.read_parquet(MODELS_FILE)
        if 'id' in df_raw.columns and 'version' in df_raw.columns:
            df = df_raw.sort_values('version').groupby('id', as_index=False).last()
        else:
            df = df_raw
    else:
        return {}

    total = len(df)
    por_tipo = {}
    algo_counts = {}
    lang_counts = {}
    metric_keys = set()
    metric_values = {k: [] for k in METRIC_KEYS_CANON}
    campos_faltantes = []

    for _, r in df.iterrows():
        # tipos y conteos
        mt = r.get('model_type') or r.get('payload.modelType')
        if mt:
            por_tipo[mt] = por_tipo.get(mt, 0) + 1
        alg = r.get('algorithm') or r.get('payload.algorithm')
        if alg:
            algo_counts[alg] = algo_counts.get(alg, 0) + 1
        lang = r.get('programming_language') or r.get('payload.scoreCodeType')
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        # métricas (busca columnas metric.<k>)
        for k in METRIC_KEYS_CANON:
            col = f'metric.{k}'
            if col in r and pd.notna(r[col]):
                try:
                    v = float(r[col])
                    metric_values[k].append(v)
                    metric_keys.add(k)
                except Exception:
                    pass

        # campos faltantes promedio: verificar core
        core_fields = [r.get('name') or r.get('payload.name'), r.get('algorithm') or r.get('payload.algorithm'), mt, lang]
        missing = sum(1 for x in core_fields if x in (None, '', []))
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
