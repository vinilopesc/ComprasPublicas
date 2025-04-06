import React from 'react';

const Footer = () => {
  const year = new Date().getFullYear();
  
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">
              &copy; {year} Sistema de Consulta ao Banco de Preços do TCE-MG
            </p>
            <p className="text-xs text-gray-400 mt-1">
              Este sistema é uma ferramenta não oficial para consulta de dados públicos
            </p>
          </div>
          
          <div className="flex space-x-4">
            <a
              href="https://bancodepreco.tce.mg.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 text-sm"
            >
              Site Oficial TCE-MG
            </a>
            <a
              href="https://www.tce.mg.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 text-sm"
            >
              Portal TCE-MG
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 