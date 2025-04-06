"""
Camada de Domínio - Contém as entidades, objetos de valor e regras de negócio
do sistema de consulta de preços do TCE-MG.
"""

from domain.entities import Product, Territory, TerritoryType, PriceRecord
from domain.value_objects import ProductFilter, TerritoryScope, PricePeriod
from domain.repositories import ProductRepository, TerritoryRepository, PriceRepository
from domain.services import ProductService, TerritoryService, PriceService

__all__ = [
    'Product',
    'Territory',
    'TerritoryType',
    'PriceRecord',
    'ProductFilter',
    'TerritoryScope',
    'PricePeriod',
    'ProductRepository',
    'TerritoryRepository',
    'PriceRepository',
    'ProductService',
    'TerritoryService',
    'PriceService'
] 