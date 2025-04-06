import pandas as pd
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from io import BytesIO

from ..config import Config

class ExcelExportService:
    """Serviço para exportação de dados para Excel."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def export_to_excel(
        self,
        data: List[Dict[str, Any]],
        filename: str = None,
        sheet_name: str = "Dados"
    ) -> BytesIO:
        """
        Exporta dados para um arquivo Excel.
        
        Args:
            data: Lista de dicionários com os dados
            filename: Nome do arquivo (opcional)
            sheet_name: Nome da planilha
            
        Returns:
            BytesIO contendo o arquivo Excel
        """
        # Cria um DataFrame pandas com os dados
        df = pd.DataFrame(data)
        
        # Gera um nome de arquivo se não foi fornecido
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.xlsx"
        
        # Verifica se o nome do arquivo termina com .xlsx
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        
        # Caminho completo do arquivo
        file_path = os.path.join(Config.EXPORT_DIR, filename)
        
        # Cria um buffer em memória para o arquivo
        output = BytesIO()
        
        # Exporta para Excel
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Retorna ao início do buffer
        output.seek(0)
        
        # Salva uma cópia no disco se necessário
        with open(file_path, "wb") as f:
            f.write(output.getvalue())
        
        self.logger.info(f"Arquivo Excel exportado: {file_path}")
        
        return output 