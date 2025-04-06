"""
Aplicativo completo para consulta ao Banco de Preços do TCE-MG
"""

import os
import sys
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, Path, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from io import BytesIO
import re
from datetime import datetime

# Adiciona o diretório atual ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura variáveis de ambiente mínimas
os.environ.setdefault("TCE_API_BASE_URL", "https://bancodepreco.tce.mg.gov.br/api/public")

# Configuração inicial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importa módulos e classes necessários
try:
    # DTOs
    from application.dtos import ProductDTO, TerritoryDTO, PriceRecordDTO

    # Configurações
    from infrastructure.config import Config
    
    # Serviços de Infraestrutura
    from infrastructure.cache.cache_service import CacheService
    from infrastructure.external.tce_mg_api_client import TCEMGApiClient
    from infrastructure.export.excel_export_service import ExcelExportService
    
    # Repositórios
    from infrastructure.repositories.tce_mg_product_repository import TCEMGProductRepository
    from infrastructure.repositories.tce_mg_territory_repository import TCEMGTerritoryRepository
    from infrastructure.repositories.tce_mg_price_repository import TCEMGPriceRepository
    
    # Serviços de Domínio
    from domain.services import ProductService, TerritoryService, PriceService
    
    # Controladores
    from application.controllers import ProductController, TerritoryController, PriceController, ExportController
except ImportError as e:
    logger.error(f"Erro ao importar módulos: {e}")
    raise

# Inicializa a configuração
Config.setup()

# Cria os serviços de infraestrutura
cache_service = CacheService()
api_client = TCEMGApiClient()
export_service = ExcelExportService()

# Cria os repositórios
product_repository = TCEMGProductRepository(api_client, cache_service)
territory_repository = TCEMGTerritoryRepository(api_client, cache_service)
price_repository = TCEMGPriceRepository(api_client, cache_service)

# Cria os serviços de domínio
product_service = ProductService(product_repository)
territory_service = TerritoryService(territory_repository)
price_service = PriceService(price_repository)

# Cria os controladores
product_controller = ProductController(product_service)
territory_controller = TerritoryController(territory_service)
price_controller = PriceController(price_service, product_service)
export_controller = ExportController(export_service)

# Cria a aplicação FastAPI
app = FastAPI(
    title="API de Consulta ao Banco de Preços do TCE-MG",
    description="API para consulta de preços de produtos em compras públicas do estado de Minas Gerais",
    version="1.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz para verificar se a API está funcionando
@app.get("/")
def root():
    return {"message": "API de Consulta ao Banco de Preços do TCE-MG está funcionando!"}

# Rotas de produtos
@app.get("/api/products/search", response_model=List[ProductDTO])
async def search_products(
    q: str = Query(..., min_length=3, description="Termo para busca de produtos")
):
    """
    Busca produtos pelo termo de pesquisa.
    
    Args:
        q: Termo para busca
        
    Returns:
        Lista de produtos encontrados
    """
    return await product_controller.search_products(q)

@app.get("/api/products/{product_id}", response_model=ProductDTO)
async def get_product(
    product_id: str = Path(..., description="ID do produto")
):
    """
    Obtém um produto pelo ID.
    
    Args:
        product_id: ID do produto
        
    Returns:
        Produto encontrado
    """
    return await product_controller.get_product(product_id)

# Rotas de territórios
@app.get("/api/regions", response_model=List[TerritoryDTO])
async def get_regions():
    """
    Obtém todas as regiões disponíveis.
    
    Returns:
        Lista de regiões
    """
    return await territory_controller.get_regions()

@app.get("/api/municipalities", response_model=List[TerritoryDTO])
async def get_municipalities(
    region_code: Optional[str] = Query(None, description="Código da região para filtrar")
):
    """
    Obtém todos os municípios, opcionalmente filtrados por região.
    
    Args:
        region_code: Código da região para filtrar (opcional)
        
    Returns:
        Lista de municípios
    """
    return await territory_controller.get_municipalities(region_code)

# Rotas de preços
@app.get("/api/prices/history", response_model=List[PriceRecordDTO])
async def get_price_history(
    product_id: str = Query(..., description="ID do produto"),
    unit: str = Query(..., description="Unidade do produto"),
    territory_type: str = Query(..., description="Tipo de território (ESTADO, REGIAO, MUNICIPIO)"),
    region_codes: Optional[List[str]] = Query(None, description="Lista de códigos de região"),
    municipality_codes: Optional[List[str]] = Query(None, description="Lista de códigos de município"),
    year: Optional[int] = Query(None, description="Ano de referência")
):
    """
    Obtém o histórico de preços de acordo com os parâmetros.
    
    Args:
        product_id: ID do produto
        unit: Unidade do produto
        territory_type: Tipo de território
        region_codes: Lista de códigos de região (opcional)
        municipality_codes: Lista de códigos de município (opcional)
        year: Ano de referência (opcional)
        
    Returns:
        Lista de registros de preço
    """
    return await price_controller.get_price_history(
        product_id=product_id,
        unit=unit,
        territory_type=territory_type,
        region_codes=region_codes,
        municipality_codes=municipality_codes,
        year=year
    )

@app.get("/api/prices/export")
async def export_price_history(
    product_id: str = Query(..., description="ID do produto"),
    product_name: str = Query(..., description="Nome do produto"),
    unit: str = Query(..., description="Unidade do produto"),
    territory_type: str = Query(..., description="Tipo de território (ESTADO, REGIAO, MUNICIPIO)"),
    region_codes: Optional[List[str]] = Query(None, description="Lista de códigos de região"),
    municipality_codes: Optional[List[str]] = Query(None, description="Lista de códigos de município"),
    year: Optional[int] = Query(None, description="Ano de referência")
):
    """
    Exporta o histórico de preços para um arquivo Excel.
    
    Args:
        product_id: ID do produto
        product_name: Nome do produto
        unit: Unidade do produto
        territory_type: Tipo de território
        region_codes: Lista de códigos de região (opcional)
        municipality_codes: Lista de códigos de município (opcional)
        year: Ano de referência (opcional)
        
    Returns:
        Arquivo Excel para download
    """
    # Obtém o histórico de preços
    price_records = await price_controller.get_price_history(
        product_id=product_id,
        unit=unit,
        territory_type=territory_type,
        region_codes=region_codes,
        municipality_codes=municipality_codes,
        year=year
    )
    
    # Exporta para Excel
    excel_content = export_controller.export_price_history_to_excel(
        price_records=price_records,
        product_name=product_name,
        unit=unit
    )
    
    # Define o nome do arquivo para download
    product_slug = re.sub(r'[^a-zA-Z0-9]', '_', product_name.lower())
    product_slug = re.sub(r'_+', '_', product_slug)
    product_slug = product_slug[:30]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"historico_precos_{product_slug}_{timestamp}.xlsx"
    
    # Retorna o arquivo como resposta
    return StreamingResponse(
        BytesIO(excel_content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Rota de informações do servidor
@app.get("/api/info")
def get_info():
    """
    Obtém informações sobre o servidor e a API.
    
    Returns:
        Informações do servidor
    """
    return {
        "api_version": "1.0.0",
        "description": "API para consulta de preços de produtos em compras públicas do estado de Minas Gerais",
        "endpoints": [
            {"path": "/api/products/search", "method": "GET", "description": "Busca produtos pelo termo de pesquisa"},
            {"path": "/api/products/{product_id}", "method": "GET", "description": "Obtém um produto pelo ID"},
            {"path": "/api/regions", "method": "GET", "description": "Obtém todas as regiões disponíveis"},
            {"path": "/api/municipalities", "method": "GET", "description": "Obtém todos os municípios, opcionalmente filtrados por região"},
            {"path": "/api/prices/history", "method": "GET", "description": "Obtém o histórico de preços de acordo com os parâmetros"},
            {"path": "/api/prices/export", "method": "GET", "description": "Exporta o histórico de preços para um arquivo Excel"}
        ]
    }

# Executa o servidor se o script for executado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 