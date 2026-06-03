# api-agregacao-clima
# API de Agregação de Dados Climáticos

Projeto desenvolvido para a disciplina Técnicas de Integração de Sistemas (N703).

## Descrição

API REST que integra APIs públicas para consulta de dados climáticos e geográficos de cidades brasileiras.

## Tecnologias Utilizadas

* Python
* FastAPI
* Requests
* Pytest

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
```

```text
http://localhost:3000
```

## Endpoints

### Health Check

```http
GET /api/v1/health
```

### Clima por Cidade
```http
GET /api/v1/clima/Fortaleza
```

### Cidades por Estado

```http
GET /api/v1/cidades/CE
```

