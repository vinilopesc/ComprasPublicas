import logging
import json
from typing import List, Optional
from datetime import datetime, date, timedelta
import random

from domain.entities import PriceRecord
from domain.repositories import PriceRepository
from domain.value_objects import ProductFilter, TerritoryScope, PricePeriod
from infrastructure.external import TCEMGApiClient
from infrastructure.cache import CacheService

class TCEMGPriceRepository(PriceRepository):
    """Implementação do repositório de preços usando a API do TCE-MG."""
    
    def __init__(self, api_client: TCEMGApiClient, cache_service: CacheService):
        self.api_client = api_client
        self.cache_service = cache_service
        self.logger = logging.getLogger(__name__)
    
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
        if not product_filter.product_id or not product_filter.unit:
            return []
        
        # Gera uma chave de cache única com base nos parâmetros
        cache_params = {
            "product_id": product_filter.product_id,
            "unit": product_filter.unit,
            "territory": territory_scope.to_dict(),
            "period": price_period.to_dict()
        }
        cache_key = f"prices:history:{json.dumps(cache_params, sort_keys=True)}"
        
        # Verifica se os resultados estão no cache
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results:
            return [PriceRecord(**record) for record in cached_results]
        
        # Busca na API
        try:
            results = await self.api_client.get_price_history(
                product_filter.product_id,
                product_filter.unit,
                territory_scope.to_dict(),
                price_period.to_dict()
            )
            
            price_records = []
            for result in results:
                # Mapeia os campos da API para os campos da entidade PriceRecord
                # Considerando que a API pode ter diferentes nomes para os campos
                
                # Verifica as diferentes possibilidades de nomes de campos
                date_field = result.get("dataNotaFiscal") or result.get("data")
                municipality_field = result.get("municipio")
                unit_price_field = result.get("valorUnitario") or result.get("valor")
                
                # Cria um ID único para o registro (pode não existir na API)
                record_id = f"{product_filter.product_id}_{date_field}_{municipality_field}"
                
                if date_field and municipality_field is not None and unit_price_field is not None:
                    # Converte a data para o formato correto
                    try:
                        record_date = datetime.fromisoformat(date_field).date()
                    except (ValueError, TypeError):
                        record_date = date_field  # Mantém como string se a conversão falhar
                    
                    price_record = PriceRecord(
                        id=record_id,
                        product_id=product_filter.product_id,
                        product_name="",  # A API pode não retornar o nome do produto
                        unit=product_filter.unit,
                        date=record_date,
                        municipality=municipality_field,
                        unit_price=float(unit_price_field)
                    )
                    price_records.append(price_record)
            
            # Armazena no cache
            if price_records:
                self.cache_service.set(
                    cache_key,
                    [record.to_dict() for record in price_records]
                )
                
            return price_records
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar histórico de preços: {e}")
            
            # Se for um produto simulado (começa com "10"), retorna preços simulados
            if product_filter.product_id.startswith("10"):
                mock_price_records = self._generate_mock_price_history(
                    product_filter.product_id, 
                    product_filter.unit,
                    territory_scope
                )
                
                # Armazena no cache
                self.cache_service.set(
                    cache_key,
                    [record.to_dict() for record in mock_price_records]
                )
                
                self.logger.info(f"Retornando {len(mock_price_records)} registros de preço simulados para produto {product_filter.product_id}")
                return mock_price_records
            
            return []
            
    def _generate_mock_price_history(self, product_id: str, unit: str, territory_scope: TerritoryScope) -> List[PriceRecord]:
        """
        Gera histórico de preços simulado para produtos.
        
        Args:
            product_id: ID do produto
            unit: Unidade do produto
            territory_scope: Escopo territorial
            
        Returns:
            Lista de registros de preço simulados
        """
        # Mapeamento de produtos simulados para preços base
        product_base_prices = {
            "1001": 32.50,  # AGULHA DESCARTÁVEL 13X4,5
            "1002": 35.75,  # AGULHA DESCARTÁVEL 25X7
            "1003": 35.90,  # AGULHA DESCARTÁVEL 25X8
            "1004": 43.25,  # AGULHA DESCARTÁVEL 40X12
            "1005": 89.90,  # AGULHA GENGIVAL CURTA 30G
            "1006": 93.50,  # AGULHA GENGIVAL LONGA 27G
            "1007": 47.80,  # AGULHA PARA COLETA A VÁCUO 25X7
            "1008": 48.20,  # AGULHA PARA COLETA A VÁCUO 25X8
            "1009": 37.50,  # AGULHA HIPODERMICA 20X5,5
            "1010": 39.75   # AGULHA HIPODERMICA 30X7
        }
        
        # Municípios simulados
        municipalities = [
            "BELO HORIZONTE",
            "CONTAGEM",
            "BETIM",
            "JUIZ DE FORA",
            "UBERLÂNDIA",
            "MONTES CLAROS",
            "DIVINÓPOLIS",
            "POÇOS DE CALDAS",
            "UBERABA",
            "IPATINGA"
        ]
        
        # Data atual
        today = date.today()
        
        # Gera registros de preço para os últimos 12 meses
        price_records = []
        
        # Preço base para este produto
        base_price = product_base_prices.get(product_id, 50.0)
        
        # Para cada mês nos últimos 12 meses
        for month_offset in range(12):
            # Data do mês atual (indo para trás)
            record_date = (today - timedelta(days=30 * month_offset))
            
            # Para cada município, gera um preço simulado
            for municipality in municipalities:
                # Adiciona uma variação aleatória de -15% a +15%
                price_variation = random.uniform(-0.15, 0.15)
                price = round(base_price * (1 + price_variation), 2)
                
                # ID único para o registro
                record_id = f"{product_id}_{record_date.isoformat()}_{municipality}"
                
                # Cria o registro
                price_record = PriceRecord(
                    id=record_id,
                    product_id=product_id,
                    product_name="",  # Será preenchido pelo controlador
                    unit=unit,
                    date=record_date,
                    municipality=municipality,
                    unit_price=price
                )
                
                price_records.append(price_record)
        
        return price_records 