import logging
from datetime import datetime
from typing import Optional, Any

from ..config import Config

class CacheService:
    """Serviço de cache em memória."""
    
    def __init__(self):
        self.cache = {}
        self.expiration_times = {}
        self.logger = logging.getLogger(__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém um valor do cache.
        
        Args:
            key: Chave do cache
            
        Returns:
            Valor armazenado ou None se não existir ou estiver expirado
        """
        if not Config.CACHE_ENABLED:
            return None
        
        current_time = datetime.now().timestamp()
        
        if key in self.cache and key in self.expiration_times:
            # Verifica se o cache expirou
            if current_time < self.expiration_times[key]:
                self.logger.debug(f"Cache hit para {key}")
                return self.cache[key]
            else:
                # Remove o item expirado
                self.logger.debug(f"Cache expirado para {key}")
                del self.cache[key]
                del self.expiration_times[key]
                
        return None
    
    def set(self, key: str, value: Any, expiration: int = None) -> None:
        """
        Armazena um valor no cache.
        
        Args:
            key: Chave do cache
            value: Valor a ser armazenado
            expiration: Tempo de expiração em segundos (opcional, usa o padrão se None)
        """
        if not Config.CACHE_ENABLED:
            return
        
        expiration = expiration or Config.CACHE_EXPIRATION
        expiration_time = datetime.now().timestamp() + expiration
        
        self.cache[key] = value
        self.expiration_times[key] = expiration_time
        
        self.logger.debug(f"Item armazenado no cache: {key}")
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
        self.expiration_times.clear()
        self.logger.debug("Cache limpo")
    
    def clear_by_prefix(self, prefix: str) -> None:
        """
        Limpa todos os itens do cache que começam com o prefixo.
        
        Args:
            prefix: Prefixo para filtrar as chaves
        """
        keys_to_remove = [key for key in self.cache.keys() if key.startswith(prefix)]
        
        for key in keys_to_remove:
            del self.cache[key]
            if key in self.expiration_times:
                del self.expiration_times[key]
        
        self.logger.debug(f"Cache limpo para o prefixo: {prefix}") 