"""
Camada de Infraestrutura - Contém as implementações concretas dos repositórios,
serviços de acesso a APIs externas, banco de dados e outras infraestruturas.
"""

from infrastructure.config import Config
from infrastructure.cache import CacheService
from infrastructure.external import TCEMGApiClient
from infrastructure.export import ExcelExportService
from infrastructure.repositories import TCEMGProductRepository, TCEMGTerritoryRepository, TCEMGPriceRepository

__all__ = [
    'Config',
    'CacheService',
    'TCEMGApiClient',
    'ExcelExportService',
    'TCEMGProductRepository',
    'TCEMGTerritoryRepository',
    'TCEMGPriceRepository'
] 