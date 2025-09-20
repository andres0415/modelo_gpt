
# ML & GenAI Model Registry

Herramienta full-stack para registrar modelos de ML e IA generativa a partir de JSON o formulario, gestionar versionamiento, consolidar master data en CSV/Parquet dentro del repo y visualizar insights en un dashboard.

## 🚀 Stack
- **Backend**: FastAPI + Pandas/PyArrow (persistencia basada en Parquet/CSV).
- **Frontend**: React (Vite) + TailwindCSS.
- **Contenedores**: Docker Compose.

## 📂 Estructura
```
lovable-ml-registry/
  backend/
    app/
      main.py
      models/ (pydantic schemas)
      routers/
        models.py
        exports.py
        dashboard.py
      services/
        model_service.py  # persistencia basada en Parquet
        master.py         # generación de exports desde models.parquet
      routers/
        models.py
        exports.py
        dashboard.py
      services/
        master.py
      utils/
        json_flatten.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      pages/
        Dashboard.tsx
        Models.tsx
        Register.tsx
      App.tsx
      api.ts
      main.tsx
      styles.css
    package.json
    Dockerfile
    vite.config.ts
    tailwind.config.js
    postcss.config.js
    index.html
  data/
    input_jsons/  <-- coloca aquí tus JSON
    exports/      <-- aquí se crearán master_latest.* y master_all.*
  docker-compose.yml
```

## 🧩 Módulos
- **Registro**: vía formulario o carga de **JSON** (objeto único o lista). Ediciones crean un nuevo registro con versión (se conserva historial en `data/models.parquet`).
- **Consolidado**: listado de **últimas versiones** con búsqueda.
- **Dashboard**: insights: algoritmo más usado, conteo por tipo (supervised/unsupervised/generative), top lenguajes, promedios de métricas (accuracy, precision, recall, f1, roc_auc, rmse, mae, mape, bleu, rouge, perplexity), y promedio de **campos faltantes** entre los core (`name`, `algorithm`, `model_type`, `programming_language`).
-- **Master data**: `data/models.parquet` contiene los registros; `data/exports/master_latest.(csv|parquet)` y `master_all.(csv|parquet)` se generan a partir de ese archivo y contienen el payload aplanado.

## 🎨 UI / Colores
Paleta predominante: **morado/violeta** y **blanco**, con acentos **gris** y **azul** (Tailwind `primary`, `neutral`, `secondary.blue`).

## ⚙️ Puesta en marcha

### Local (sin Docker)
Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn app.main:app --reload --port 8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

La aplicación expone:
- Backend: http://localhost:8000 (Swagger: `/docs`)
- Frontend: http://localhost:5173

Configura `VITE_API_BASE` en el frontend si el backend no está en `http://localhost:8000`.

## 📥 Ingesta de tus JSON
Coloca tus archivos `.json` en `data/input_jsons/` y luego:
- Vía API (archivo): `POST /models/from-json-file` (multipart `file` con JSON)
- Vía API (objeto): `POST /models` (body JSON)

También puedes generar exports manualmente:

```bash
curl -X POST http://localhost:8000/exports/rebuild
```

Cada objeto JSON puede contener campos libres. El backend detecta automáticamente claves comunes (`name`, `algorithm`, `model_type`, `programming_language`, `metrics`, `tags`). Todo el objeto se guarda como `raw_payload` y se aplanará en la master.

## ✍️ Registro y edición
- **Registrar (formulario)** desde la UI o `POST /models` con body JSON.
- **Registrar (archivo)** `POST /models/from-json-file` con multipart `file` (objeto o lista de objetos). El endpoint devuelve el objeto registrado y la ruta absoluta al `master_latest.parquet` generado.
- **Editar** `PUT /models/<built-in function id>/edit` crea **nueva versión** en el mismo `model_group_id` y actualiza master.

## 📊 Exports & Dashboard
- Re-generar master: `POST /exports/rebuild`
- Insights: `GET /dashboard/insights`

## 🔌 Esquema flexible
No necesitas adaptar tus JSON a un esquema rígido. Para versionamiento consistente entre ediciones, puedes enviar/guardar `model_group_id` en tu JSON; si no, el sistema crea uno nuevo.

## Notas sobre cambios recientes
- Migración a persistencia basada en Parquet/CSV (`backend/app/services/model_service.py`).
- `backend/app/services/master.py` genera los exports en `data/exports`.
- Los archivos legacy basados en SQLModel han sido movidos a `backend/app/legacy/`.
- Se agregó un test unitario y un workflow CI (`.github/workflows/ci.yml`).

## ✅ Checklist rápido en Lovable
1. Crea un nuevo proyecto y sube este repositorio.
2. Ajusta `VITE_API_BASE` si usas un dominio propio.
3. Coloca tus JSON en `data/input_jsons/` y ejecuta **Bulk Ingest**.
4. Verifica `data/exports/master_latest.parquet` generado.

---

**Siguientes mejoras sugeridas** (opcionales):
- Autenticación y control de permisos.
- Campos obligatorios parametrizables y validaciones por tipo de modelo.
- Soporte para adjuntar artefactos (p.ej., ruta a modelo, checksum, registro de features, etc.).
- Integración con DuckDB para consultas analíticas avanzadas.
- Gráficos interactivos con charting libs.

