import logging
from typing import List, Optional
import json

from domain.entities import Territory, TerritoryType
from domain.repositories import TerritoryRepository
from infrastructure.external import TCEMGApiClient
from infrastructure.cache import CacheService

class TCEMGTerritoryRepository(TerritoryRepository):
    """Implementação do repositório de territórios usando a API do TCE-MG."""
    
    def __init__(self, api_client: TCEMGApiClient, cache_service: CacheService):
        self.api_client = api_client
        self.cache_service = cache_service
        self.logger = logging.getLogger(__name__)
    
    async def get_regions(self) -> List[Territory]:
        """
        Obtém todas as regiões disponíveis.
        
        Returns:
            Lista de regiões
        """
        # Verifica se as regiões estão no cache
        cache_key = "territories:regions"
        cached_regions = self.cache_service.get(cache_key)
        
        if cached_regions:
            return [Territory(**region) for region in cached_regions]
        
        # Busca na API
        try:
            results = await self.api_client.get_regions()
            
            regions = []
            for result in results:
                region_id = result.get("id") or result.get("codigo")
                region_name = result.get("nome")
                
                if region_id and region_name:
                    region = Territory(
                        id=region_id,
                        name=region_name,
                        type=TerritoryType.REGION
                    )
                    regions.append(region)
            
            # Armazena no cache
            self.cache_service.set(
                cache_key,
                [region.to_dict() for region in regions]
            )
            
            return regions
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar regiões: {e}")
            
            # Fallback para regiões fixas em caso de erro
            # Este é apenas um exemplo, as regiões reais devem ser obtidas da API
            fallback_regions = [
                Territory("1", "Central", TerritoryType.REGION),
                Territory("2", "Zona da Mata", TerritoryType.REGION),
                Territory("3", "Sul de Minas", TerritoryType.REGION),
                Territory("4", "Triângulo Mineiro", TerritoryType.REGION),
                Territory("5", "Alto Paranaíba", TerritoryType.REGION),
                Territory("6", "Centro-Oeste", TerritoryType.REGION),
                Territory("7", "Noroeste", TerritoryType.REGION),
                Territory("8", "Norte", TerritoryType.REGION),
                Territory("9", "Jequitinhonha/Mucuri", TerritoryType.REGION),
                Territory("10", "Rio Doce", TerritoryType.REGION)
            ]
            
            # Armazena no cache
            self.cache_service.set(
                cache_key,
                [region.to_dict() for region in fallback_regions]
            )
            
            return fallback_regions
    
    async def get_municipalities(self, region_code: str = None) -> List[Territory]:
        """
        Obtém todos os municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região para filtrar (opcional)
            
        Returns:
            Lista de municípios
        """
        # Verifica se os municípios estão no cache
        cache_key = f"territories:municipalities:{region_code or 'all'}"
        cached_municipalities = self.cache_service.get(cache_key)
        
        if cached_municipalities:
            return [Territory(**municipality) for municipality in cached_municipalities]
        
        # Busca na API
        try:
            results = await self.api_client.get_municipalities(region_code)
            
            municipalities = []
            for result in results:
                municipality_id = result.get("id") or result.get("codigo")
                municipality_name = result.get("nome")
                
                if municipality_id and municipality_name:
                    municipality = Territory(
                        id=municipality_id,
                        name=municipality_name,
                        type=TerritoryType.MUNICIPALITY
                    )
                    municipalities.append(municipality)
            
            # Armazena no cache
            self.cache_service.set(
                cache_key,
                [municipality.to_dict() for municipality in municipalities]
            )
            
            return municipalities
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar municípios: {e}")
            
            # Fallback para municípios fixos em caso de erro
            # Limitamos a lista para os maiores municípios de Minas Gerais
            # Filtramos por região se necessário
            
            all_municipalities = [
                Territory("3106200", "BELO HORIZONTE", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3106705", "CONTAGEM", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3106200", "BETIM", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3136702", "JUIZ DE FORA", TerritoryType.MUNICIPALITY, region_id="2"),
                Territory("3170206", "UBERLÂNDIA", TerritoryType.MUNICIPALITY, region_id="4"),
                Territory("3143302", "MONTES CLAROS", TerritoryType.MUNICIPALITY, region_id="8"),
                Territory("3122306", "DIVINÓPOLIS", TerritoryType.MUNICIPALITY, region_id="6"),
                Territory("3151800", "POÇOS DE CALDAS", TerritoryType.MUNICIPALITY, region_id="3"),
                Territory("3170107", "UBERABA", TerritoryType.MUNICIPALITY, region_id="4"),
                Territory("3131307", "IPATINGA", TerritoryType.MUNICIPALITY, region_id="10"),
                Territory("3153905", "RIBEIRÃO DAS NEVES", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3154606", "SANTA LUZIA", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3129806", "GOVERNADOR VALADARES", TerritoryType.MUNICIPALITY, region_id="10"),
                Territory("3156700", "SETE LAGOAS", TerritoryType.MUNICIPALITY, region_id="1"),
                Territory("3118601", "CORONEL FABRICIANO", TerritoryType.MUNICIPALITY, region_id="10"),
                Territory("3171204", "VARGINHA", TerritoryType.MUNICIPALITY, region_id="3"),
                Territory("3149309", "PATOS DE MINAS", TerritoryType.MUNICIPALITY, region_id="5"),
                Territory("3127701", "FORMIGA", TerritoryType.MUNICIPALITY, region_id="6"),
                Territory("3140159", "LAVRAS", TerritoryType.MUNICIPALITY, region_id="3"),
                Territory("3161809", "TEÓFILO OTONI", TerritoryType.MUNICIPALITY, region_id="9")
            ]
            
            # Filtra por região, se necessário
            if region_code:
                filtered_municipalities = [m for m in all_municipalities if m.region_id == region_code]
            else:
                filtered_municipalities = all_municipalities
            
            # Armazena no cache
            self.cache_service.set(
                cache_key,
                [municipality.to_dict() for municipality in filtered_municipalities]
            )
            
            return filtered_municipalities
    
    async def get_territory(self, territory_id: str, territory_type: TerritoryType) -> Optional[Territory]:
        """
        Obtém um território específico pelo ID e tipo.
        
        Args:
            territory_id: ID do território
            territory_type: Tipo do território
            
        Returns:
            Território encontrado ou None
        """
        # Verifica se o território está no cache
        cache_key = f"territories:{territory_type.value}:{territory_id}"
        cached_territory = self.cache_service.get(cache_key)
        
        if cached_territory:
            return Territory(**cached_territory)
        
        # Busca de acordo com o tipo
        if territory_type == TerritoryType.REGION:
            regions = await self.get_regions()
            for region in regions:
                if region.id == territory_id:
                    # Armazena no cache
                    self.cache_service.set(cache_key, region.to_dict())
                    return region
        
        elif territory_type == TerritoryType.MUNICIPALITY:
            municipalities = await self.get_municipalities()
            for municipality in municipalities:
                if municipality.id == territory_id:
                    # Armazena no cache
                    self.cache_service.set(cache_key, municipality.to_dict())
                    return municipality
        
        return None 