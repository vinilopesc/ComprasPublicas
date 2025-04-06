"""
Módulo para implementações concretas dos repositórios de domínio.
"""

from infrastructure.repositories.tce_mg_product_repository import TCEMGProductRepository
from infrastructure.repositories.tce_mg_territory_repository import TCEMGTerritoryRepository
from infrastructure.repositories.tce_mg_price_repository import TCEMGPriceRepository

__all__ = [
    'TCEMGProductRepository',
    'TCEMGTerritoryRepository',
    'TCEMGPriceRepository'
] 