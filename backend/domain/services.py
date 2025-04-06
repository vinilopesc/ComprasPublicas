from typing import List, Optional
from domain.entities import Product, Territory, TerritoryType, PriceRecord
from domain.repositories import ProductRepository, TerritoryRepository, PriceRepository
from domain.value_objects import ProductFilter, TerritoryScope, PricePeriod

class ProductService:
    """Serviço de domínio para operações relacionadas a produtos."""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def search_products(self, search_term: str) -> List[Product]:
        """
        Busca produtos por termo de pesquisa.
        
        Args:
            search_term: Termo para busca
            
        Returns:
            Lista de produtos encontrados
        """
        product_filter = ProductFilter(search_term=search_term)
        return await self.product_repository.search_products(product_filter)
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """
        Obtém um produto pelo ID.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Produto encontrado ou None
        """
        return await self.product_repository.get_product(product_id)


class TerritoryService:
    """Serviço de domínio para operações relacionadas a territórios."""
    
    def __init__(self, territory_repository: TerritoryRepository):
        self.territory_repository = territory_repository
    
    async def get_regions(self) -> List[Territory]:
        """
        Obtém todas as regiões disponíveis.
        
        Returns:
            Lista de regiões
        """
        return await self.territory_repository.get_regions()
    
    async def get_municipalities(self, region_code: str = None) -> List[Territory]:
        """
        Obtém todos os municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região para filtrar (opcional)
            
        Returns:
            Lista de municípios
        """
        return await self.territory_repository.get_municipalities(region_code)


class PriceService:
    """Serviço de domínio para operações relacionadas a preços."""
    
    def __init__(self, price_repository: PriceRepository):
        self.price_repository = price_repository
    
    async def get_price_history(
        self,
        product_id: str,
        unit: str,
        territory_type: str,
        region_codes: List[str] = None,
        municipality_codes: List[str] = None,
        year: int = None
    ) -> List[PriceRecord]:
        """
        Obtém o histórico de preços de acordo com os parâmetros especificados.
        
        Args:
            product_id: ID do produto
            unit: Unidade do produto
            territory_type: Tipo de território (estado, região, município)
            region_codes: Lista de códigos de região (opcional)
            municipality_codes: Lista de códigos de município (opcional)
            year: Ano de referência (opcional)
            
        Returns:
            Lista de registros de preço
        """
        # Converte a string do tipo de território para o enum
        territory_enum = TerritoryType(territory_type)
        
        product_filter = ProductFilter(product_id=product_id, unit=unit)
        
        territory_scope = TerritoryScope(
            territory_type=territory_enum,
            region_codes=region_codes,
            municipality_codes=municipality_codes
        )
        
        price_period = PricePeriod(year=year)
        
        return await self.price_repository.get_price_history(
            product_filter,
            territory_scope,
            price_period
        ) 