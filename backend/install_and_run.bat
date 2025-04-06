@echo off
echo Instalando dependências...
pip install fastapi==0.95.0 uvicorn==0.21.1 pydantic==1.10.7 aiohttp==3.8.4 pandas==1.5.3 numpy==1.23.5 openpyxl==3.1.2 python-dotenv==1.0.0 python-jose==3.3.0 passlib==1.7.4 bcrypt==4.0.1 loguru==0.7.0 python-multipart==0.0.6

echo.
echo Executando aplicação...
python app.py 