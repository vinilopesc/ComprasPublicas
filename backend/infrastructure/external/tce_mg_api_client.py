import aiohttp
import logging
from typing import Dict, Any, List, Optional

from ..config import Config

class TCEMGApiClient:
    """Cliente para a API do Banco de Preços do TCE-MG."""
    
    def __init__(self):
        self.session = None
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """Inicializa a sessão HTTP."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fecha a sessão HTTP."""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Realiza uma requisição GET para a API.
        
        Args:
            url: URL da requisição
            params: Parâmetros da requisição
            
        Returns:
            Resposta da API em formato JSON
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            self.logger.debug(f"Requisição GET para {url} com parâmetros: {params}")
            
            async with self.session.get(url, params=params) as response:
                # Se a resposta for 404, registramos o erro e retornamos um array vazio
                if response.status == 404:
                    self.logger.error(f"Erro na requisição para {url}: {response.status}, message='', url={response.url}")
                    return []
                
                # Para outros erros, levantamos a exceção normalmente
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"Erro na requisição para {url}: {e}")
            raise
        except aiohttp.ClientError as e:
            self.logger.error(f"Erro na requisição para {url}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na requisição para {url}: {e}")
            raise
    
    async def search_products(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Busca produtos pelo termo de pesquisa.
        
        Args:
            search_term: Termo de busca
            
        Returns:
            Lista de produtos encontrados
        """
        try:
            params = {"descricao": search_term}
            results = await self.get(Config.TCE_PRODUCTS_ENDPOINT, params)
            return results if isinstance(results, list) else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar produtos com termo '{search_term}': {e}")
            return []
    
    async def get_regions(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de regiões disponíveis.
        
        Returns:
            Lista de regiões
        """
        try:
            results = await self.get(Config.TCE_REGIONS_ENDPOINT)
            return results if isinstance(results, list) else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar regiões: {e}")
            return []
    
    async def get_municipalities(self, region_code: str = None) -> List[Dict[str, Any]]:
        """
        Obtém a lista de municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região (opcional)
            
        Returns:
            Lista de municípios
        """
        try:
            params = {}
            if region_code:
                params["codRegiao"] = region_code
                
            results = await self.get(Config.TCE_MUNICIPALITIES_ENDPOINT, params)
            return results if isinstance(results, list) else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar municípios: {e}")
            return []
    
    async def get_price_history(
        self,
        product_id: str,
        unit: str,
        territory_scope: Dict[str, Any],
        period: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Obtém o histórico de preços de acordo com os parâmetros.
        
        Args:
            product_id: ID do produto
            unit: Unidade do produto
            territory_scope: Escopo territorial
            period: Período de tempo
            
        Returns:
            Lista de registros de preço
        """
        try:
            params = {
                "idProduto": product_id,
                "unidade": unit
            }
            
            # Adiciona parâmetros de escopo territorial
            params.update(territory_scope)
            
            # Adiciona parâmetros de período
            params.update(period)
            
            results = await self.get(Config.TCE_PRICE_HISTORY_ENDPOINT, params)
            return results if isinstance(results, list) else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar histórico de preços para produto {product_id}: {e}")
            return [] 