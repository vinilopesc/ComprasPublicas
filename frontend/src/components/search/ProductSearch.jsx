import React, { useState, useEffect, useRef } from 'react';
import { useQuery } from 'react-query';
import { Search, X } from 'lucide-react';
import { debounce } from 'lodash';
import { searchProducts } from '../../services/api';

const ProductSearch = ({ onProductSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const searchRef = useRef(null);
  
  // Debounce a busca para evitar muitas requisições
  const debouncedSearch = useRef(
    debounce(async (term) => {
      if (term.length >= 3) {
        refetch();
      }
    }, 300)
  ).current;
  
  // Hook para fechar o dropdown quando clicar fora
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [searchRef]);
  
  // React Query para buscar produtos
  const { data, isLoading, refetch } = useQuery(
    ['products', searchTerm],
    () => searchProducts(searchTerm),
    {
      enabled: false,
      keepPreviousData: true,
    }
  );
  
  // Efeito para realizar a busca quando o termo mudar
  useEffect(() => {
    if (searchTerm.length >= 3) {
      debouncedSearch(searchTerm);
    }
  }, [searchTerm, debouncedSearch]);
  
  // Manipulador para mudar o termo de busca
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    if (value.length >= 3) {
      setShowResults(true);
    } else {
      setShowResults(false);
    }
    
    if (selectedProduct) {
      setSelectedProduct(null);
      onProductSelect(null);
    }
  };
  
  // Manipulador para selecionar um produto
  const handleSelectProduct = (product) => {
    setSelectedProduct(product);
    setSearchTerm(product.name);
    setShowResults(false);
    onProductSelect(product);
  };
  
  // Manipulador para limpar a busca
  const handleClearSearch = () => {
    setSearchTerm('');
    setSelectedProduct(null);
    setShowResults(false);
    onProductSelect(null);
  };
  
  return (
    <div className="relative w-full" ref={searchRef}>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        
        <input
          type="text"
          value={searchTerm}
          onChange={handleSearchChange}
          onFocus={() => searchTerm.length >= 3 && setShowResults(true)}
          placeholder="Digite o nome do produto (ex: caneta, papel, combustível)"
          className="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        />
        
        {searchTerm && (
          <button
            onClick={handleClearSearch}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>
      
      {showResults && searchTerm.length >= 3 && (
        <div className="absolute z-10 w-full mt-1 bg-white shadow-lg rounded-lg max-h-96 overflow-y-auto border border-gray-200">
          {isLoading && (
            <div className="p-4 text-center text-gray-500">
              <div className="animate-spin inline-block w-5 h-5 border-t-2 border-blue-500 border-r-2 border-b-2 border-transparent rounded-full mr-2"></div>
              Buscando produtos...
            </div>
          )}
          
          {!isLoading && data && data.length === 0 && (
            <div className="p-4 text-center text-gray-500">
              Nenhum produto encontrado para "{searchTerm}"
            </div>
          )}
          
          {!isLoading && data && data.length > 0 && (
            <ul className="py-2">
              {data.map((product) => (
                <li
                  key={product.id}
                  onClick={() => handleSelectProduct(product)}
                  className="px-4 py-2 hover:bg-blue-50 cursor-pointer flex justify-between items-center"
                >
                  <div>
                    <div className="font-medium">{product.name}</div>
                    <div className="text-sm text-gray-500">ID: {product.id}</div>
                  </div>
                  <div className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
                    {product.unit}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
      
      {selectedProduct && (
        <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex justify-between items-center">
            <div>
              <div className="font-medium text-blue-800">{selectedProduct.name}</div>
              <div className="text-sm text-blue-600">
                ID: {selectedProduct.id} | Unidade: {selectedProduct.unit}
              </div>
            </div>
            <button
              onClick={handleClearSearch}
              className="text-blue-500 hover:text-blue-700"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductSearch; 