import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Database, Search, Home, Info } from 'lucide-react';

const Header = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'bg-blue-700' : '';
  };
  
  return (
    <header className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          <div className="flex items-center space-x-2">
            <Database size={24} />
            <h1 className="text-xl font-bold">Consulta Banco de Preços TCE-MG</h1>
          </div>
          
          <nav>
            <ul className="flex space-x-1">
              <li>
                <Link
                  to="/"
                  className={`px-3 py-2 rounded flex items-center space-x-1 hover:bg-blue-700 ${isActive('/')}`}
                >
                  <Home size={18} />
                  <span>Início</span>
                </Link>
              </li>
              <li>
                <Link
                  to="/search"
                  className={`px-3 py-2 rounded flex items-center space-x-1 hover:bg-blue-700 ${isActive('/search')}`}
                >
                  <Search size={18} />
                  <span>Consultar</span>
                </Link>
              </li>
              <li>
                <Link
                  to="/about"
                  className={`px-3 py-2 rounded flex items-center space-x-1 hover:bg-blue-700 ${isActive('/about')}`}
                >
                  <Info size={18} />
                  <span>Sobre</span>
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 