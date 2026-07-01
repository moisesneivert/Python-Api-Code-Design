# Guia de instalação e publicação

Este guia apresenta os comandos para preparar o projeto no Windows com PowerShell,
executar a API no Visual Studio Code e publicar as alterações no GitHub.

## Requisitos

- Python 3.12 ou 3.13
- Git
- Visual Studio Code
- Docker Desktop, opcional

## Ambiente virtual

```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-dev.txt
```

## Executar

```powershell
Copy-Item .env.example .env
python run.py
```

Acesse:

- API: `http://127.0.0.1:5000`
- Swagger UI: `http://127.0.0.1:5000/docs`
- OpenAPI: `http://127.0.0.1:5000/openapi.json`
- Saúde: `http://127.0.0.1:5000/health`

## Qualidade

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Docker

```powershell
docker compose up --build
```

## Conectar ao repositório existente

Quando a pasta veio de um ZIP e não contém `.git`:

```powershell
git init
git branch -M main
git remote add origin https://github.com/moisesneivert/Python-Api-Code-Design.git
git fetch origin
git reset origin/main
```

Depois valide e publique:

```powershell
git add -A
git status
git commit -m "feat: rebuild calculation API with clean architecture"
git push -u origin main
```
