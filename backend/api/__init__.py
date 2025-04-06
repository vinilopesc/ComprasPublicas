"""
Camada de API - Contém as rotas da API e a configuração do servidor FastAPI.
"""

from api.server import app, create_app, run
from api.dependencies import Dependencies

__all__ = ['app', 'create_app', 'run', 'Dependencies'] 