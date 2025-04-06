from pydantic import BaseModel
from typing import Optional
from datetime import date

from domain.entities import Product, Territory, PriceRecord

class ProductDTO(BaseModel):
    """DTO para representação de produtos na API."""
    id: str
    name: str
    unit: str
    
    @classmethod
    def from_entity(cls, entity: Product) -> 'ProductDTO':
        """
        Converte uma entidade de domínio para DTO.
        
        Args:
            entity: Entidade de produto
            
        Returns:
            DTO de produto
        """
        return cls(
            id=entity.id,
            name=entity.name,
            unit=entity.unit
        )


class TerritoryDTO(BaseModel):
    """DTO para representação de territórios na API."""
    id: str
    name: str
    type: str
    region_id: Optional[str] = None
    
    @classmethod
    def from_entity(cls, entity: Territory) -> 'TerritoryDTO':
        """
        Converte uma entidade de domínio para DTO.
        
        Args:
            entity: Entidade de território
            
        Returns:
            DTO de território
        """
        return cls(
            id=entity.id,
            name=entity.name,
            type=entity.type.value,
            region_id=entity.region_id
        )


class PriceRecordDTO(BaseModel):
    """DTO para representação de registros de preço na API."""
    id: str
    product_id: str
    product_name: str
    unit: str
    date: date
    municipality: str
    unit_price: float
    
    @classmethod
    def from_entity(cls, entity: PriceRecord) -> 'PriceRecordDTO':
        """
        Converte uma entidade de domínio para DTO.
        
        Args:
            entity: Entidade de registro de preço
            
        Returns:
            DTO de registro de preço
        """
        return cls(
            id=entity.id,
            product_id=entity.product_id,
            product_name=entity.product_name,
            unit=entity.unit,
            date=entity.date if isinstance(entity.date, date) else date.fromisoformat(entity.date),
            municipality=entity.municipality,
            unit_price=entity.unit_price
        ) 