
"""
Archivo legacy `models.py` (deprecated).
La lógica de persistencia fue migrada a `backend/app/services/model_service.py` y los exports se generan
en `data/exports`. Si necesitas la versión antigua basada en SQLModel, revisa `backend/app/legacy/models.py`.
"""

from warnings import warn

warn('backend.app.models is deprecated. Use backend.app.services.model_service for persistence.')
