"""
Servidor FastAPI para a API do sistema de consulta ao Banco de Preços do TCE-MG.
"""

from fastapi import FastAPI, Query, Path, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
import logging
import asyncio
from io import BytesIO
import re
from datetime import datetime

# Importações absolutas em vez de relativas
from api.dependencies import Dependencies
from application.controllers import ProductController, TerritoryController, PriceController, ExportController
from application.dtos import ProductDTO, TerritoryDTO, PriceRecordDTO

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.
    
    Returns:
        Aplicação FastAPI configurada
    """
    # Cria a aplicação
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
    
    # Inicializa as dependências
    dependencies = Dependencies()
    
    # Define as rotas
    
    # Rotas de produtos
    @app.get("/api/products/search", response_model=List[ProductDTO])
    async def search_products(
        q: str = Query(..., min_length=3, description="Termo para busca de produtos"),
        product_controller: ProductController = Depends(dependencies.get_product_controller)
    ):
        """
        Busca produtos pelo termo de pesquisa.
        
        Args:
            q: Termo para busca
            product_controller: Controlador de produtos
            
        Returns:
            Lista de produtos encontrados
        """
        return await product_controller.search_products(q)
    
    @app.get("/api/products/{product_id}", response_model=ProductDTO)
    async def get_product(
        product_id: str = Path(..., description="ID do produto"),
        product_controller: ProductController = Depends(dependencies.get_product_controller)
    ):
        """
        Obtém um produto pelo ID.
        
        Args:
            product_id: ID do produto
            product_controller: Controlador de produtos
            
        Returns:
            Produto encontrado
        """
        return await product_controller.get_product(product_id)
    
    # Rotas de territórios
    @app.get("/api/regions", response_model=List[TerritoryDTO])
    async def get_regions(
        territory_controller: TerritoryController = Depends(dependencies.get_territory_controller)
    ):
        """
        Obtém todas as regiões disponíveis.
        
        Args:
            territory_controller: Controlador de territórios
            
        Returns:
            Lista de regiões
        """
        return await territory_controller.get_regions()
    
    @app.get("/api/municipalities", response_model=List[TerritoryDTO])
    async def get_municipalities(
        region_code: Optional[str] = Query(None, description="Código da região para filtrar"),
        territory_controller: TerritoryController = Depends(dependencies.get_territory_controller)
    ):
        """
        Obtém todos os municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região para filtrar (opcional)
            territory_controller: Controlador de territórios
            
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
        year: Optional[int] = Query(None, description="Ano de referência"),
        price_controller: PriceController = Depends(dependencies.get_price_controller)
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
            price_controller: Controlador de preços
            
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
        year: Optional[int] = Query(None, description="Ano de referência"),
        price_controller: PriceController = Depends(dependencies.get_price_controller),
        export_controller: ExportController = Depends(dependencies.get_export_controller)
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
            price_controller: Controlador de preços
            export_controller: Controlador de exportação
            
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
    
    return app


# Criação da aplicação
app = create_app()


# Função para executar a aplicação
def run():
    """Executa a aplicação com uvicorn."""
    import uvicorn
    
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 