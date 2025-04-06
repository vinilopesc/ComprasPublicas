import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Calendar, MapPin } from 'lucide-react';
import { toast } from 'react-toastify';

import ProductSearch from '../components/search/ProductSearch';
import TerritorySelector from '../components/search/TerritorySelector';

const SearchPage = () => {
  const navigate = useNavigate();
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [territory, setTerritory] = useState({
    type: 'ESTADO',
    regionCodes: [],
    municipalityCodes: []
  });
  const [year, setYear] = useState('');
  
  // Manipulador para a mudança de produto selecionado
  const handleProductSelect = (product) => {
    setSelectedProduct(product);
  };
  
  // Manipulador para a mudança de território
  const handleTerritoryChange = (territoryData) => {
    setTerritory(territoryData);
  };
  
  // Manipulador para a mudança de ano
  const handleYearChange = (e) => {
    setYear(e.target.value);
  };
  
  // Manipulador para submissão do formulário
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validação
    if (!selectedProduct) {
      toast.error('Selecione um produto para continuar');
      return;
    }
    
    if (territory.type === 'REGIAO' && territory.regionCodes.length === 0) {
      toast.error('Selecione pelo menos uma região');
      return;
    }
    
    if (territory.type === 'MUNICIPIO' && territory.municipalityCodes.length === 0) {
      toast.error('Selecione pelo menos um município');
      return;
    }
    
    // Constrói os parâmetros para a consulta
    const params = {
      product_id: selectedProduct.id,
      product_name: selectedProduct.name,
      unit: selectedProduct.unit,
      territory_type: territory.type
    };
    
    // Adiciona códigos de região se necessário
    if (territory.type === 'REGIAO' && territory.regionCodes.length > 0) {
      params.region_codes = territory.regionCodes;
    }
    
    // Adiciona códigos de município se necessário
    if (territory.type === 'MUNICIPIO' && territory.municipalityCodes.length > 0) {
      params.municipality_codes = territory.municipalityCodes;
    }
    
    // Adiciona ano se fornecido
    if (year) {
      params.year = parseInt(year, 10);
    }
    
    // Navega para a página de resultados com os parâmetros na URL
    navigate('/results', { state: params });
  };
  
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Consulta de Preços</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Search className="mr-2 text-blue-600" size={20} />
            Produto
          </h2>
          <p className="text-gray-600 mb-4">
            Digite o nome do produto que deseja consultar, por exemplo: "caneta", "papel A4", etc.
          </p>
          <ProductSearch onProductSelect={handleProductSelect} />
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <MapPin className="mr-2 text-blue-600" size={20} />
            Território
          </h2>
          <p className="text-gray-600 mb-4">
            Selecione o limite territorial para a consulta. Pode ser todo o estado, regiões específicas ou municípios.
          </p>
          <TerritorySelector onTerritoryChange={handleTerritoryChange} />
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Calendar className="mr-2 text-blue-600" size={20} />
            Período
          </h2>
          <p className="text-gray-600 mb-4">
            Selecione o ano para a consulta de preços. Deixe em branco para considerar todos os anos disponíveis.
          </p>
          <div className="w-full">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Ano (opcional):
            </label>
            <select
              value={year}
              onChange={handleYearChange}
              className="block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todos os anos</option>
              {/* Anos disponíveis - ajuste conforme necessário */}
              {[2023, 2022, 2021, 2020, 2019, 2018].map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Consultar Preços
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchPage; 