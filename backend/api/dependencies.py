"""
Gerenciamento de dependências para injeção na API FastAPI.
"""

import logging
from typing import Optional

# Importações absolutas em vez de relativas
from domain.services import ProductService, TerritoryService, PriceService
from application.controllers import ProductController, TerritoryController, PriceController, ExportController
from infrastructure.config import Config
from infrastructure.external import TCEMGApiClient
from infrastructure.cache import CacheService
from infrastructure.export import ExcelExportService
from infrastructure.repositories import TCEMGProductRepository, TCEMGTerritoryRepository, TCEMGPriceRepository

class Dependencies:
    """
    Gerencia as dependências da aplicação usando o padrão Singleton.
    Facilita o uso com o sistema de injeção de dependências do FastAPI.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Dependencies, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            # Inicializa os serviços e repositórios
            self.initialize()
            self._initialized = True
    
    def initialize(self):
        """Inicializa todas as dependências da aplicação."""
        # Configura a aplicação
        Config.setup()
        
        # Cria os serviços de infraestrutura
        self.cache_service = CacheService()
        self.api_client = TCEMGApiClient()
        self.export_service = ExcelExportService()
        
        # Cria os repositórios
        self.product_repository = TCEMGProductRepository(self.api_client, self.cache_service)
        self.territory_repository = TCEMGTerritoryRepository(self.api_client, self.cache_service)
        self.price_repository = TCEMGPriceRepository(self.api_client, self.cache_service)
        
        # Cria os serviços de domínio
        self.product_service = ProductService(self.product_repository)
        self.territory_service = TerritoryService(self.territory_repository)
        self.price_service = PriceService(self.price_repository)
        
        # Cria os controladores
        self.product_controller = ProductController(self.product_service)
        self.territory_controller = TerritoryController(self.territory_service)
        self.price_controller = PriceController(self.price_service, self.product_service)
        self.export_controller = ExportController(self.export_service)
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    async def get_api_client(self):
        """
        Obtém o cliente da API do TCE-MG com contexto assíncrono.
        
        Returns:
            Cliente da API
        """
        async with self.api_client as client:
            yield client
    
    def get_product_controller(self) -> ProductController:
        """
        Obtém o controlador de produtos.
        
        Returns:
            Controlador de produtos
        """
        return self.product_controller
    
    def get_territory_controller(self) -> TerritoryController:
        """
        Obtém o controlador de territórios.
        
        Returns:
            Controlador de territórios
        """
        return self.territory_controller
    
    def get_price_controller(self) -> PriceController:
        """
        Obtém o controlador de preços.
        
        Returns:
            Controlador de preços
        """
        return self.price_controller
    
    def get_export_controller(self) -> ExportController:
        """
        Obtém o controlador de exportação.
        
        Returns:
            Controlador de exportação
        """
        return self.export_controller 