import React from 'react';
import { Link } from 'react-router-dom';
import { Search, Database, FileText, BarChart } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="py-8">
      <div className="text-center max-w-3xl mx-auto mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Banco de Preços de Compras Públicas
        </h1>
        <p className="text-xl text-gray-600">
          Consulte e analise preços praticados em compras públicas 
          realizadas no estado de Minas Gerais.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-4">
            <div className="bg-blue-100 p-3 rounded-full mr-4">
              <Search className="h-6 w-6 text-blue-600" />
            </div>
            <h2 className="text-xl font-semibold">Consultar Preços</h2>
          </div>
          <p className="text-gray-600 mb-4">
            Pesquise produtos e veja os preços praticados em diferentes municípios e regiões.
          </p>
          <Link
            to="/search"
            className="inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
          >
            Iniciar Consulta
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-4">
            <div className="bg-green-100 p-3 rounded-full mr-4">
              <BarChart className="h-6 w-6 text-green-600" />
            </div>
            <h2 className="text-xl font-semibold">Análise de Preços</h2>
          </div>
          <p className="text-gray-600 mb-4">
            Visualize gráficos e estatísticas para análise comparativa de preços.
          </p>
          <Link
            to="/search" 
            className="inline-block bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition-colors"
          >
            Ver Análises
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-4">
            <div className="bg-purple-100 p-3 rounded-full mr-4">
              <Database className="h-6 w-6 text-purple-600" />
            </div>
            <h2 className="text-xl font-semibold">Banco de Dados</h2>
          </div>
          <p className="text-gray-600 mb-4">
            Acesse o banco de dados oficial do TCE-MG com milhares de registros de compras.
          </p>
          <a
            href="https://bancodepreco.tce.mg.gov.br/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 transition-colors"
          >
            Visitar Site Oficial
          </a>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-4">
            <div className="bg-amber-100 p-3 rounded-full mr-4">
              <FileText className="h-6 w-6 text-amber-600" />
            </div>
            <h2 className="text-xl font-semibold">Sobre o Sistema</h2>
          </div>
          <p className="text-gray-600 mb-4">
            Saiba mais sobre o funcionamento do sistema e como utilizar as funcionalidades.
          </p>
          <Link
            to="/about"
            className="inline-block bg-amber-600 text-white py-2 px-4 rounded hover:bg-amber-700 transition-colors"
          >
            Mais Informações
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 