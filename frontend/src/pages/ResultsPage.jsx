import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { ArrowLeft, AlertTriangle } from 'lucide-react';
import { toast } from 'react-toastify';

import { getPriceHistory } from '../services/api';
import Loading from '../components/common/Loading';
import ErrorDisplay from '../components/common/ErrorDisplay';
import PriceTable from '../components/results/PriceTable';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const searchParams = location.state;
  
  // Verificar se temos os parâmetros necessários
  useEffect(() => {
    if (!searchParams || !searchParams.product_id) {
      toast.error('Parâmetros de consulta inválidos');
      navigate('/search');
    }
  }, [searchParams, navigate]);
  
  // Obter o histórico de preços
  const { data, isLoading, error, refetch } = useQuery(
    ['priceHistory', searchParams],
    () => getPriceHistory(searchParams),
    {
      enabled: !!searchParams,
      refetchOnWindowFocus: false,
    }
  );
  
  // Função para voltar à página de busca
  const handleBackToSearch = () => {
    navigate('/search');
  };
  
  // Se não temos parâmetros, não renderiza nada
  if (!searchParams) {
    return null;
  }
  
  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Histórico de Preços</h1>
        <button
          onClick={handleBackToSearch}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-600 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <ArrowLeft size={16} className="mr-2" />
          Voltar para a consulta
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Detalhes da Consulta</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">Produto</p>
            <p className="text-base text-gray-900">{searchParams.product_name}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Unidade</p>
            <p className="text-base text-gray-900">{searchParams.unit}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Território</p>
            <p className="text-base text-gray-900">
              {searchParams.territory_type === 'ESTADO' && 'Todo o Estado'}
              {searchParams.territory_type === 'REGIAO' && 'Por Região'}
              {searchParams.territory_type === 'MUNICIPIO' && 'Por Município'}
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Ano</p>
            <p className="text-base text-gray-900">
              {searchParams.year || 'Todos os anos disponíveis'}
            </p>
          </div>
        </div>
      </div>
      
      {isLoading && <Loading message="Consultando dados de preços..." />}
      
      {error && (
        <ErrorDisplay
          error={error}
          retry={() => refetch()}
        />
      )}
      
      {data && data.length === 0 && !isLoading && !error && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                Nenhum registro de preço encontrado para os critérios selecionados. 
                Tente modificar os parâmetros da consulta.
              </p>
            </div>
          </div>
        </div>
      )}
      
      {data && data.length > 0 && (
        <PriceTable data={data} searchParams={searchParams} />
      )}
    </div>
  );
};

export default ResultsPage; 