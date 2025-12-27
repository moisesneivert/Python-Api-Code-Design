# Python API – Code Design & Best Practices

API simples em Python para cálculo de média aritmética, desenvolvida com foco em **boas práticas de design de código**, separação de responsabilidades e testes automatizados.

## Objetivo
Demonstrar domínio de:
- arquitetura básica de APIs REST
- organização de código
- testes unitários
- validação de dados

## Tecnologias
- Python 3
- Flask
- Pytest

## Como executar

```bash
git clone https://github.com/moisesneivert/python-api-code-design.git
cd python-api-code-design
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

## Executando com Docker

```bash
docker build -t python-api-code-design .
docker run -p 5000:5000 python-api-code-design

## Testes

O projeto possui testes unitários e de integração.

```bash
pytest

## Documentação da API (Swagger)

A API possui documentação automática via Swagger.

Após iniciar a aplicação, acesse:

http://localhost:5000/apidocs
