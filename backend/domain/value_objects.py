from datetime import date
from typing import List, Optional
from domain.entities import TerritoryType

class ProductFilter:
    """Objeto de valor que representa um filtro de produto."""
    
    def __init__(self, search_term: str = None, product_id: str = None, unit: str = None):
        self.search_term = search_term
        self.product_id = product_id
        self.unit = unit
    
    def to_dict(self) -> dict:
        result = {}
        if self.search_term:
            result["descricao"] = self.search_term
        if self.product_id:
            result["idProduto"] = self.product_id
        if self.unit:
            result["unidade"] = self.unit
        return result


class TerritoryScope:
    """Objeto de valor que representa o escopo territorial de uma consulta."""
    
    def __init__(
        self,
        territory_type: TerritoryType,
        region_codes: Optional[List[str]] = None,
        municipality_codes: Optional[List[str]] = None
    ):
        self.territory_type = territory_type
        self.region_codes = region_codes if region_codes else []
        self.municipality_codes = municipality_codes if municipality_codes else []
    
    def to_dict(self) -> dict:
        result = {
            "limiteTerritorial": self.territory_type.value
        }
        
        if self.territory_type == TerritoryType.REGION and self.region_codes:
            result["codRegioes"] = ",".join(self.region_codes)
        
        if self.territory_type == TerritoryType.MUNICIPALITY and self.municipality_codes:
            result["codMunicipios"] = ",".join(self.municipality_codes)
        
        return result


class PricePeriod:
    """Objeto de valor que representa o período de tempo para consulta de preços."""
    
    def __init__(
        self,
        year: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
    
    def to_dict(self) -> dict:
        result = {}
        
        if self.year:
            result["exercicio"] = str(self.year)
        
        if self.start_date:
            result["dataInicial"] = self.start_date.isoformat()
        
        if self.end_date:
            result["dataFinal"] = self.end_date.isoformat()
        
        return result 