# Financeiro API

API do sistema de controle financeiro familiar: FastAPI (Python 3.12) + MongoDB.

## Como rodar

```
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
uvicorn app.main:app --reload
```

## Qualidade

```
ruff check . ; black --check . ; mypy app ; pytest
```

O pre-commit fica na raiz do monorepo (`.pre-commit-config.yaml`). Instale uma vez, a partir da raiz:

```
pre-commit install
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md).
