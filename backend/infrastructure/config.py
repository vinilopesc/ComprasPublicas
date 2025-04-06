import os
import logging
from dotenv import load_dotenv

class Config:
    """Configurações da aplicação."""
    
    # URLs da API do TCE-MG
    TCE_API_BASE_URL = "https://bancodepreco.tce.mg.gov.br/api/public"
    TCE_PRODUCTS_ENDPOINT = f"{TCE_API_BASE_URL}/produtos"
    TCE_REGIONS_ENDPOINT = f"{TCE_API_BASE_URL}/regioes"  # Endpoint hipotético
    TCE_MUNICIPALITIES_ENDPOINT = f"{TCE_API_BASE_URL}/municipios"  # Endpoint hipotético
    TCE_PRICE_HISTORY_ENDPOINT = f"{TCE_API_BASE_URL}/precos/historico"
    
    # Configurações de cache
    CACHE_ENABLED = True
    CACHE_EXPIRATION = 3600  # 1 hora em segundos
    
    # Configurações de logging
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Diretório para armazenar arquivos exportados
    EXPORT_DIR = "exports"
    
    @classmethod
    def setup(cls):
        """Configura a aplicação."""
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Sobrescreve configurações com variáveis de ambiente se existirem
        if os.getenv("TCE_API_BASE_URL"):
            cls.TCE_API_BASE_URL = os.getenv("TCE_API_BASE_URL")
            cls.TCE_PRODUCTS_ENDPOINT = f"{cls.TCE_API_BASE_URL}/produtos"
            cls.TCE_REGIONS_ENDPOINT = f"{cls.TCE_API_BASE_URL}/regioes"
            cls.TCE_MUNICIPALITIES_ENDPOINT = f"{cls.TCE_API_BASE_URL}/municipios"
            cls.TCE_PRICE_HISTORY_ENDPOINT = f"{cls.TCE_API_BASE_URL}/precos/historico"
            
        if os.getenv("CACHE_ENABLED"):
            cls.CACHE_ENABLED = os.getenv("CACHE_ENABLED").lower() in ["true", "1", "t", "y", "yes"]
            
        if os.getenv("CACHE_EXPIRATION"):
            cls.CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION"))
            
        if os.getenv("LOG_LEVEL"):
            level_name = os.getenv("LOG_LEVEL").upper()
            level = getattr(logging, level_name, logging.INFO)
            cls.LOG_LEVEL = level
            
        if os.getenv("EXPORT_DIR"):
            cls.EXPORT_DIR = os.getenv("EXPORT_DIR")
        
        # Configura o logging
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format=cls.LOG_FORMAT
        )
        
        # Cria o diretório de exportação se não existir
        if not os.path.exists(cls.EXPORT_DIR):
            os.makedirs(cls.EXPORT_DIR) 