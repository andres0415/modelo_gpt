"""
Archivo legacy `database.py` (deprecated).
La lógica de persistencia de archivos fue movida a `backend/app/services/model_service.py`.
Si necesitas la versión antigua, revisa `backend/app/legacy/database.py`.
"""

from warnings import warn

warn('backend.app.database is deprecated. Use backend.app.services.model_service for persistence.')
