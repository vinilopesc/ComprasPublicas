# Sistema de Consulta ao Banco de Preços do TCE-MG

Sistema para consulta e análise de preços de produtos em compras públicas realizadas no estado de Minas Gerais, utilizando dados disponibilizados pela API do Tribunal de Contas do Estado.

## Configuração e Execução

### Requisitos

- Python 3.9 ou superior
- Node.js 14 ou superior
- npm ou yarn

### Backend (Método Rápido)

1. Navegue para o diretório backend:
   ```
   cd Compras_publicas_novo/backend
   ```

2. Ative o ambiente virtual que você já criou:
   ```
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/MacOS
   ```

3. Execute o script de instalação e execução:
   ```
   # Windows
   .\install_and_run.bat
   
   # Linux/MacOS
   chmod +x install_and_run.sh
   ./install_and_run.sh
   ```

### Backend (Método Manual)

Se o método rápido não funcionar, siga estas etapas:

1. Navegue para o diretório backend:
   ```
   cd Compras_publicas_novo/backend
   ```

2. Ative o ambiente virtual que você já criou:
   ```
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/MacOS
   ```

3. Instale as dependências manualmente:
   ```
   pip install fastapi uvicorn pydantic aiohttp pandas openpyxl python-dotenv
   ```

4. Execute a aplicação com:
   ```
   python run_app.py
   ```

### Solução de Problemas do Backend

Se você encontrar erros relacionados a importações, tente:

1. Verificar se o seu ambiente virtual está ativado
2. Instalar mais pacotes se necessário:
   ```
   pip install -e .
   ```
3. Se o erro for "ImportError: attempted relative import beyond top-level package", use o `run_app.py` em vez de `main.py`:
   ```
   python run_app.py
   ```

### Frontend

1. Navegue para o diretório frontend:
   ```
   cd Compras_publicas_novo/frontend
   ```

2. Instale as dependências:
   ```
   npm install
   # ou
   yarn install
   ```

3. Execute o servidor de desenvolvimento:
   ```
   npm start
   # ou
   yarn start
   ```

## Uso da API

A documentação completa da API está disponível em `http://localhost:8000/docs` quando o servidor backend estiver em execução.

## Estrutura do Projeto

O sistema é dividido em duas partes principais:

- **Backend**: API REST desenvolvida com Python/FastAPI, seguindo uma arquitetura em camadas (Domain, Application, Infrastructure, API).
- **Frontend**: Interface de usuário desenvolvida com React.

## Avisos

Este sistema é uma ferramenta não oficial para consulta dos dados do Banco de Preços do TCE-MG. Não há garantias de precisão dos dados ou continuidade da disponibilidade da API. 