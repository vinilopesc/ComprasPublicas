import React from 'react';
import { AlertTriangle } from 'lucide-react';

const ErrorDisplay = ({ error, retry }) => {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6 my-6">
      <div className="flex items-start">
        <div className="shrink-0">
          <AlertTriangle className="h-6 w-6 text-red-500" />
        </div>
        <div className="ml-3">
          <h3 className="text-lg font-medium text-red-800">Erro ao carregar dados</h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{error?.message || 'Ocorreu um erro inesperado'}</p>
          </div>
          {retry && (
            <div className="mt-4">
              <button
                onClick={retry}
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Tentar novamente
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorDisplay; 