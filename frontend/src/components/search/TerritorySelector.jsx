import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { getRegions, getMunicipalities } from '../../services/api';
import Loading from '../common/Loading';
import ErrorDisplay from '../common/ErrorDisplay';

const TerritorySelector = ({ onTerritoryChange }) => {
  const [territoryType, setTerritoryType] = useState('ESTADO');
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [selectedMunicipalities, setSelectedMunicipalities] = useState([]);
  const [selectedRegionForFilter, setSelectedRegionForFilter] = useState('');
  
  // Busca regiões
  const { 
    data: regions, 
    isLoading: isLoadingRegions, 
    error: regionsError,
    refetch: refetchRegions 
  } = useQuery('regions', getRegions);
  
  // Busca municípios, possivelmente filtrados por região
  const {
    data: municipalities,
    isLoading: isLoadingMunicipalities,
    error: municipalitiesError,
    refetch: refetchMunicipalities
  } = useQuery(
    ['municipalities', selectedRegionForFilter], 
    () => getMunicipalities(selectedRegionForFilter),
    {
      enabled: territoryType === 'MUNICIPIO'
    }
  );
  
  // Atualiza o território quando os valores mudam
  useEffect(() => {
    const territoryData = {
      type: territoryType,
      regionCodes: selectedRegions,
      municipalityCodes: selectedMunicipalities
    };
    
    onTerritoryChange(territoryData);
  }, [territoryType, selectedRegions, selectedMunicipalities, onTerritoryChange]);
  
  // Manipula a mudança do tipo de território
  const handleTerritoryTypeChange = (e) => {
    const newType = e.target.value;
    setTerritoryType(newType);
    
    // Limpa seleções anteriores
    if (newType === 'ESTADO') {
      setSelectedRegions([]);
      setSelectedMunicipalities([]);
    }
    
    // Carrega dados necessários
    if (newType === 'MUNICIPIO' && !municipalities) {
      refetchMunicipalities();
    }
  };
  
  // Manipula a seleção de regiões
  const handleRegionChange = (e) => {
    const options = e.target.options;
    const selectedValues = [];
    
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selectedValues.push(options[i].value);
      }
    }
    
    setSelectedRegions(selectedValues);
  };
  
  // Manipula a seleção do filtro de região para municípios
  const handleRegionFilterChange = (e) => {
    setSelectedRegionForFilter(e.target.value);
    setSelectedMunicipalities([]);
  };
  
  // Manipula a seleção de municípios
  const handleMunicipalityChange = (e) => {
    const options = e.target.options;
    const selectedValues = [];
    
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selectedValues.push(options[i].value);
      }
    }
    
    setSelectedMunicipalities(selectedValues);
  };
  
  // Renderiza o seletor de regiões
  const renderRegionSelector = () => {
    if (isLoadingRegions) {
      return <div className="py-2 text-gray-500">Carregando regiões...</div>;
    }
    
    if (regionsError) {
      return (
        <ErrorDisplay 
          error={regionsError} 
          retry={() => refetchRegions()} 
        />
      );
    }
    
    if (regions && regions.length > 0) {
      return (
        <div className="mt-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Selecione as regiões (mantenha Ctrl pressionado para selecionar múltiplas):
          </label>
          <select
            multiple
            value={selectedRegions}
            onChange={handleRegionChange}
            className="block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 h-48"
          >
            {regions.map((region) => (
              <option key={region.id} value={region.id}>
                {region.name}
              </option>
            ))}
          </select>
          
          {selectedRegions.length > 0 && (
            <div className="mt-2 text-sm text-gray-500">
              {selectedRegions.length} {selectedRegions.length === 1 ? 'região selecionada' : 'regiões selecionadas'}
            </div>
          )}
        </div>
      );
    }
    
    return <div className="py-2 text-gray-500">Nenhuma região disponível</div>;
  };
  
  // Renderiza o seletor de municípios
  const renderMunicipalitySelector = () => {
    if (isLoadingMunicipalities) {
      return <div className="py-2 text-gray-500">Carregando municípios...</div>;
    }
    
    if (municipalitiesError) {
      return (
        <ErrorDisplay 
          error={municipalitiesError} 
          retry={() => refetchMunicipalities()} 
        />
      );
    }
    
    return (
      <div className="mt-2">
        <div className="mb-3">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Filtrar por região (opcional):
          </label>
          <select
            value={selectedRegionForFilter}
            onChange={handleRegionFilterChange}
            className="block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todos os municípios</option>
            {regions && regions.map((region) => (
              <option key={region.id} value={region.id}>
                {region.name}
              </option>
            ))}
          </select>
        </div>
        
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Selecione os municípios (mantenha Ctrl pressionado para selecionar múltiplos):
        </label>
        
        {municipalities && municipalities.length > 0 ? (
          <>
            <select
              multiple
              value={selectedMunicipalities}
              onChange={handleMunicipalityChange}
              className="block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 h-48"
            >
              {municipalities.map((municipality) => (
                <option key={municipality.id} value={municipality.id}>
                  {municipality.name}
                </option>
              ))}
            </select>
            
            {selectedMunicipalities.length > 0 && (
              <div className="mt-2 text-sm text-gray-500">
                {selectedMunicipalities.length} {selectedMunicipalities.length === 1 ? 'município selecionado' : 'municípios selecionados'}
              </div>
            )}
          </>
        ) : (
          <div className="py-2 text-gray-500">
            {selectedRegionForFilter ? "Nenhum município disponível para esta região" : "Nenhum município disponível"}
          </div>
        )}
      </div>
    );
  };
  
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Limite territorial:
      </label>
      <select
        value={territoryType}
        onChange={handleTerritoryTypeChange}
        className="block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="ESTADO">Todo o Estado</option>
        <option value="REGIAO">Por Região</option>
        <option value="MUNICIPIO">Por Município</option>
      </select>
      
      {territoryType === 'REGIAO' && renderRegionSelector()}
      {territoryType === 'MUNICIPIO' && renderMunicipalitySelector()}
    </div>
  );
};

export default TerritorySelector; 