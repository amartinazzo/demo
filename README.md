# Demo: API para um modelo de deep learning pré-treinado

### Pré-requisitos

* Instalar dependências: `pip install -f requirements.txt`

* Baixar modelo pré-treinado: `python download_model.py`

### Rodando testes

```
pytest
```

### Subindo um servidor localmente

```
uvicorn main:app --reload
```

A API estará disponível em `localhost:8000` (e os docs em `localhost:8000/docs`)