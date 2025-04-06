from datetime import date
from enum import Enum
from typing import Optional

class TerritoryType(Enum):
    """Enum que define os tipos de território disponíveis."""
    STATE = "ESTADO"
    REGION = "REGIAO"
    MUNICIPALITY = "MUNICIPIO"

class Product:
    """Entidade que representa um produto no sistema."""
    
    def __init__(self, id: str, name: str, unit: str):
        self.id = id
        self.name = name
        self.unit = unit
    
    def __str__(self) -> str:
        return f"{self.name} ({self.unit})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit
        }


class Territory:
    """Entidade que representa um território geográfico."""
    
    def __init__(self, id: str, name: str, type: TerritoryType, region_id: Optional[str] = None):
        self.id = id
        self.name = name
        self.type = type
        self.region_id = region_id
    
    def __str__(self) -> str:
        return f"{self.name} ({self.type.value})"
    
    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type.value
        }
        
        if self.region_id:
            result["region_id"] = self.region_id
            
        return result


class PriceRecord:
    """Entidade que representa um registro de preço."""
    
    def __init__(
        self, 
        id: str,
        product_id: str,
        product_name: str,
        unit: str,
        date: date,
        municipality: str,
        unit_price: float
    ):
        self.id = id
        self.product_id = product_id
        self.product_name = product_name
        self.unit = unit
        self.date = date
        self.municipality = municipality
        self.unit_price = unit_price
    
    def __str__(self) -> str:
        return f"{self.product_name} - {self.municipality} - {self.date} - R$ {self.unit_price:.2f}"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit": self.unit,
            "date": self.date.isoformat() if isinstance(self.date, date) else self.date,
            "municipality": self.municipality,
            "unit_price": self.unit_price
        } 