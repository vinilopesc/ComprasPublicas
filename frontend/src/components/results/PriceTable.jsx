import React, { useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, FileDown } from 'lucide-react';
import { createExcelDownloadUrl } from '../../services/api';

const PriceTable = ({ data, searchParams }) => {
  const [sortConfig, setSortConfig] = useState({ key: 'date', direction: 'desc' });
  
  // Função para formatar valores monetários
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };
  
  // Função para formatar datas
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR').format(date);
  };
  
  // Função para ordenar os dados da tabela
  const sortedData = React.useMemo(() => {
    if (!data) return [];
    
    let sortableItems = [...data];
    
    if (sortConfig.key) {
      sortableItems.sort((a, b) => {
        // Trata diferentes tipos de dados
        let aValue = a[sortConfig.key];
        let bValue = b[sortConfig.key];
        
        // Conversão para comparação
        if (sortConfig.key === 'date') {
          aValue = new Date(aValue);
          bValue = new Date(bValue);
        } else if (sortConfig.key === 'unit_price') {
          aValue = Number(aValue);
          bValue = Number(bValue);
        }
        
        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    
    return sortableItems;
  }, [data, sortConfig]);
  
  // Função para alterar a ordenação
  const requestSort = (key) => {
    let direction = 'asc';
    
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    
    setSortConfig({ key, direction });
  };
  
  // Função para exibir o ícone de ordenação
  const getSortIcon = (key) => {
    if (sortConfig.key !== key) {
      return <ArrowUpDown size={16} className="ml-1 text-gray-400" />;
    }
    
    return sortConfig.direction === 'asc' 
      ? <ArrowUp size={16} className="ml-1 text-blue-500" /> 
      : <ArrowDown size={16} className="ml-1 text-blue-500" />;
  };
  
  // Função para criar URL de download do Excel
  const getExcelDownloadUrl = () => {
    if (!searchParams) return '#';
    return createExcelDownloadUrl(searchParams);
  };
  
  // Se não houver dados, exibe mensagem
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <p className="text-gray-500">Nenhum registro de preço encontrado para os critérios selecionados.</p>
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 flex justify-between items-center border-b">
        <h3 className="text-lg font-medium">Resultados da Consulta</h3>
        
        <a
          href={getExcelDownloadUrl()}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <FileDown size={16} className="mr-2" />
          Exportar para Excel
        </a>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th 
                scope="col" 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => requestSort('date')}
              >
                <div className="flex items-center">
                  Data
                  {getSortIcon('date')}
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => requestSort('municipality')}
              >
                <div className="flex items-center">
                  Município
                  {getSortIcon('municipality')}
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => requestSort('unit_price')}
              >
                <div className="flex items-center">
                  Preço Unitário
                  {getSortIcon('unit_price')}
                </div>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedData.map((record) => (
              <tr key={record.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatDate(record.date)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {record.municipality}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {formatCurrency(record.unit_price)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-4 bg-gray-50 border-t text-sm text-gray-500">
        Total de {data.length} registros encontrados
      </div>
    </div>
  );
};

export default PriceTable; 