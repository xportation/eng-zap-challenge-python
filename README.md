# Code Challenge Grupo ZAP
### eng-zap-challenge-python
Realizado desafio da Opção B (fazer uma API backend)  
Link do desafio: [Code Challenge Grupo Zap](https://olxbr.github.io/cultura/challenges/engineering.html)

## Setup

As dependências para rodar a aplicação estão no arquivo `requirements.txt` e para desenvolvimento no arquivo `requirements-dev.txt`.  
  
Instalação das dependências para rodar a aplicação:

```shell
> pip3 install -r requirements.txt
```

Instalação das dependências para rodar a aplicação, desenvolver, rodar testes e relatórios:

```shell
> pip3 install -r requirements-dev.txt
```

## Rodar a aplicação

Rodar apenas localmente:

```shell
> python3 main.py
```

Utilizar o `uvicorn` para rodar em produção:

```shell
> uvicorn main:app --log-config log.ini
```

Também é possível utilizar o comando `make runserver` do Makefile para rodar localmente. 
Este comando roda o `uvicorn` com o auto **reload**.

## Docs

A documentação do Swagger é gerada automaticamente em `<url>/docs`.

http://127.0.0.1:8000/docs

## Testes e Qualidade

Comandos:

- Testes: `pytest`
- Lint: `flake8`
- Coverage: `coverage run -m pytest` e `coverage report -m` para mostrar o relatório.

Estes comandos estáo todos no Makefile.

```shell
> make test
> make coverage
> make quality
```

## API
São duas APIs:
- `[GET] http://127.0.0.1:8000/api/properties/zap`
- `[GET] http://127.0.0.1:8000/api/properties/viva-real`

Ambas as APIs possuem os seguintes filtros de `query param`:
- `pageNumber`
- `pageSize`
- `businessType`
- `city`
- `minPrice`
- `maxPrice`
- `bedrooms`
- `bathrooms`
