from typing import List, Optional
from fastapi import HTTPException, status
import logging
from datetime import datetime
import re
from io import BytesIO

from domain.entities import TerritoryType
from domain.services import ProductService, TerritoryService, PriceService
from application.dtos import ProductDTO, TerritoryDTO, PriceRecordDTO
from infrastructure.export import ExcelExportService

class ProductController:
    """Controlador para operações relacionadas a produtos."""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self.logger = logging.getLogger(__name__)
    
    async def search_products(self, search_term: str) -> List[ProductDTO]:
        """
        Busca produtos pelo termo de pesquisa.
        
        Args:
            search_term: Termo para busca
            
        Returns:
            Lista de DTOs de produtos
        """
        if not search_term or len(search_term.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O termo de busca deve ter pelo menos 3 caracteres."
            )
            
        self.logger.info(f"Buscando produtos para o termo: {search_term}")
        
        products = await self.product_service.search_products(search_term)
        
        return [ProductDTO.from_entity(product) for product in products]
    
    async def get_product(self, product_id: str) -> ProductDTO:
        """
        Obtém um produto pelo ID.
        
        Args:
            product_id: ID do produto
            
        Returns:
            DTO do produto
        """
        self.logger.info(f"Buscando produto com ID: {product_id}")
        
        product = await self.product_service.get_product(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado."
            )
            
        return ProductDTO.from_entity(product)


class TerritoryController:
    """Controlador para operações relacionadas a territórios."""
    
    def __init__(self, territory_service: TerritoryService):
        self.territory_service = territory_service
        self.logger = logging.getLogger(__name__)
    
    async def get_regions(self) -> List[TerritoryDTO]:
        """
        Obtém todas as regiões disponíveis.
        
        Returns:
            Lista de DTOs de regiões
        """
        self.logger.info("Buscando regiões")
        
        regions = await self.territory_service.get_regions()
        
        return [TerritoryDTO.from_entity(region) for region in regions]
    
    async def get_municipalities(self, region_code: str = None) -> List[TerritoryDTO]:
        """
        Obtém todos os municípios, opcionalmente filtrados por região.
        
        Args:
            region_code: Código da região para filtrar (opcional)
            
        Returns:
            Lista de DTOs de municípios
        """
        self.logger.info(f"Buscando municípios{' da região ' + region_code if region_code else ''}")
        
        municipalities = await self.territory_service.get_municipalities(region_code)
        
        return [TerritoryDTO.from_entity(municipality) for municipality in municipalities]


class PriceController:
    """Controlador para operações relacionadas a preços."""
    
    def __init__(self, price_service: PriceService, product_service: ProductService):
        self.price_service = price_service
        self.product_service = product_service
        self.logger = logging.getLogger(__name__)
    
    async def get_price_history(
        self,
        product_id: str,
        unit: str,
        territory_type: str,
        region_codes: List[str] = None,
        municipality_codes: List[str] = None,
        year: int = None
    ) -> List[PriceRecordDTO]:
        """
        Obtém o histórico de preços de acordo com os parâmetros.
        
        Args:
            product_id: ID do produto
            unit: Unidade do produto
            territory_type: Tipo de território (ESTADO, REGIAO, MUNICIPIO)
            region_codes: Lista de códigos de região (opcional)
            municipality_codes: Lista de códigos de município (opcional)
            year: Ano de referência (opcional)
            
        Returns:
            Lista de DTOs de registros de preço
        """
        self.logger.info(f"Buscando histórico de preços para produto {product_id}, unidade {unit}")
        
        # Valida o tipo de território
        try:
            territory_enum = TerritoryType(territory_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de território inválido: {territory_type}. Deve ser ESTADO, REGIAO ou MUNICIPIO."
            )
        
        # Valida a existência do produto
        product = await self.product_service.get_product(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado."
            )
        
        # Valida códigos de região/município de acordo com o tipo de território
        if territory_enum == TerritoryType.REGION and not region_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Códigos de região são obrigatórios quando o tipo de território é REGIAO."
            )
            
        if territory_enum == TerritoryType.MUNICIPALITY and not municipality_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Códigos de município são obrigatórios quando o tipo de território é MUNICIPIO."
            )
        
        # Busca o histórico de preços
        price_records = await self.price_service.get_price_history(
            product_id=product_id,
            unit=unit,
            territory_type=territory_type,
            region_codes=region_codes,
            municipality_codes=municipality_codes,
            year=year
        )
        
        # Adiciona o nome do produto aos registros
        for record in price_records:
            record.product_name = product.name
        
        return [PriceRecordDTO.from_entity(record) for record in price_records]


class ExportController:
    """Controlador para operações de exportação de dados."""
    
    def __init__(self, export_service: ExcelExportService):
        self.export_service = export_service
        self.logger = logging.getLogger(__name__)
    
    def export_price_history_to_excel(
        self,
        price_records: List[PriceRecordDTO],
        product_name: str,
        unit: str,
        filename: str = None
    ) -> bytes:
        """
        Exporta o histórico de preços para um arquivo Excel.
        
        Args:
            price_records: Lista de registros de preço
            product_name: Nome do produto
            unit: Unidade do produto
            filename: Nome do arquivo (opcional)
            
        Returns:
            Conteúdo do arquivo Excel
        """
        self.logger.info(f"Exportando histórico de preços para Excel: {product_name} ({unit})")
        
        # Converte os DTOs para dicionários
        data = [record.dict() for record in price_records]
        
        # Gera um nome de arquivo se não foi fornecido
        if not filename:
            # Cria um slug a partir do nome do produto
            product_slug = re.sub(r'[^a-zA-Z0-9]', '_', product_name.lower())
            product_slug = re.sub(r'_+', '_', product_slug)  # Remove underscores duplicados
            product_slug = product_slug[:30]  # Limita o tamanho
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historico_precos_{product_slug}_{timestamp}.xlsx"
        
        # Exporta para Excel
        excel_buffer = self.export_service.export_to_excel(
            data=data,
            filename=filename,
            sheet_name=f"{product_name} ({unit})"
        )
        
        return excel_buffer.getvalue() 