import React from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink, FileText, Info } from 'lucide-react';

const AboutPage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Sobre o Sistema</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <Info className="mr-2 text-blue-600" size={20} />
          O que é este sistema?
        </h2>
        <p className="text-gray-700 mb-4">
          Este sistema foi desenvolvido para facilitar a consulta e análise de preços de produtos em compras públicas
          realizadas no estado de Minas Gerais. Utiliza dados disponibilizados pela API do Tribunal de Contas do Estado
          (TCE-MG) através do seu Banco de Preços.
        </p>
        <p className="text-gray-700 mb-4">
          O objetivo é oferecer uma interface intuitiva e funcionalidades de análise que permitam aos gestores públicos,
          fornecedores e cidadãos tomarem decisões mais informadas sobre compras públicas.
        </p>
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-800">
            <strong>Aviso importante:</strong> Este é um sistema não oficial. Os dados são provenientes da API pública do TCE-MG,
            mas este sistema não é mantido ou endossado oficialmente pelo Tribunal de Contas do Estado de Minas Gerais.
          </p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <FileText className="mr-2 text-blue-600" size={20} />
          Como utilizar
        </h2>
        <ol className="list-decimal pl-5 space-y-4 text-gray-700">
          <li>
            <strong>Busca de produtos:</strong> Na página de consulta, você pode pesquisar produtos por nome, visualizando
            os resultados em tempo real.
          </li>
          <li>
            <strong>Seleção de território:</strong> Escolha se deseja visualizar preços em todo o estado, por região
            ou por municípios específicos.
          </li>
          <li>
            <strong>Filtro por período:</strong> Selecione o ano ou período específico para a análise.
          </li>
          <li>
            <strong>Análise de resultados:</strong> Visualize os dados em tabelas e gráficos, identificando variações
            de preços e possíveis outliers.
          </li>
          <li>
            <strong>Exportação:</strong> Exporte os resultados para Excel para análises mais detalhadas.
          </li>
        </ol>
        <div className="mt-4">
          <Link
            to="/search"
            className="inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
          >
            Ir para a Consulta
          </Link>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <ExternalLink className="mr-2 text-blue-600" size={20} />
          Recursos Externos
        </h2>
        <div className="space-y-3">
          <div>
            <a
              href="https://bancodepreco.tce.mg.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-medium"
            >
              Banco de Preços do TCE-MG
            </a>
            <p className="text-gray-700 text-sm mt-1">
              Site oficial do Banco de Preços do Tribunal de Contas do Estado de Minas Gerais.
            </p>
          </div>
          <div>
            <a
              href="https://www.tce.mg.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-medium"
            >
              Portal TCE-MG
            </a>
            <p className="text-gray-700 text-sm mt-1">
              Portal oficial do Tribunal de Contas do Estado de Minas Gerais.
            </p>
          </div>
          <div>
            <a
              href="https://receita.fazenda.gov.br/PessoaJuridica/CNPJ/cnpjreva/cnpjreva_solicitacao.asp"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-medium"
            >
              Consulta CNPJ
            </a>
            <p className="text-gray-700 text-sm mt-1">
              Consulta de CNPJ na Receita Federal para verificação de fornecedores.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage; 