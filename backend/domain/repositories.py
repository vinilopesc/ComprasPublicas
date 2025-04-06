from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Product, Territory, TerritoryType, PriceRecord
from domain.value_objects import ProductFilter, TerritoryScope, PricePeriod

class ProductRepository(ABC):
    """Interface para repositório de produtos."""
    
    @abstractmethod
    async def search_products(self, product_filter: ProductFilter) -> List[Product]:
        """
        Busca produtos de acordo com o filtro especificado.
        
        Args:
            product_filter: Filtro de busca de produtos
            
        Returns:
            Lista de produtos encontrados
        """
        pass
    
    @abstractmethod
    async def get_product(self, product_id: str) -> Optional[Product]:
        """
        Obtém um produto pelo ID.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Produto encontrado ou None
        """
        pass


class TerritoryRepository(ABC):
    """Interface para repositório de territórios."""
    
    @abstractmethod
    async def get_regions(self) -> List[Territory]:
        """
        Obtém todas as regiões disponíveis.
        
        Returns:
            Lista de regiões
        """
        pass
    
    @abstractmethod
    async def get_municipalities(self, region_code: str = None) -> List[Territory]:
        """
        Obtém todos os municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região para filtrar (opcional)
            
        Returns:
            Lista de municípios
        """
        pass
    
    @abstractmethod
    async def get_territory(self, territory_id: str, territory_type: TerritoryType) -> Optional[Territory]:
        """
        Obtém um território específico pelo ID e tipo.
        
        Args:
            territory_id: ID do território
            territory_type: Tipo do território
            
        Returns:
            Território encontrado ou None
        """
        pass


class PriceRepository(ABC):
    """Interface para repositório de preços."""
    
    @abstractmethod
    async def get_price_history(
        self,
        product_filter: ProductFilter,
        territory_scope: TerritoryScope,
        price_period: PricePeriod
    ) -> List[PriceRecord]:
        """
        Obtém o histórico de preços de acordo com os filtros especificados.
        
        Args:
            product_filter: Filtro de produto
            territory_scope: Escopo territorial
            price_period: Período de tempo
            
        Returns:
            Lista de registros de preço
        """
        pass 