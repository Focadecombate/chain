# Trabalho Tolerância a Falhas

## Alunos

- Gustavo de Almeida Freitas Santos

## Github

[Link](https://github.com/Focadecombate/chain)

## Como executar

### Requisitos

- Python 3.10
- Poetry

### Instalação

```bash
cd src
poetry install
```

### Execução

```bash
poetry run python main.py
```

## Descrição

O trabalho consiste em implementar uma blockchain como uma lista encadeada distribuída, onde cada nó é um processo. O processo deve ser capaz de se recuperar de falhas, e a lista deve ser capaz de se recuperar de falhas de nós. Temos um arquivo para armazenar os endereços dos nós e um banco de dados sqlite3 para armazenar os blocos.

## Funcionamento

### Nós

Cada nó escreve seu endereço no arquivo `sync.json` toda vez que iniciado e lê os endereços dos outros nós. A lista de nós é usada para se conectar a outros nós. A cada 5 segundos ou quando ocorre alguma mudança o estado da lista é replicado para os outros nós por meio de requisições HTTP.

### Blocos

A lista inicia com um bloco genesis e cada bloco possui um hash que é calculado a partir do hash do bloco anterior, o timestamp e o dado. O dado é uma string fornecida pelo cliente. O timestamp é o tempo em segundos desde o epoch. O hash é calculado usando a função SHA256 e um bloco precisa ter um hash valido para ser adicionado na lista.

### Blockchain

Temos rotas para adicionar blocos, obter a lista e verificar a integridade da lista.

### Health Check

A permanência de um nó no grupo é baseada em health-checks, se 3 health-checks consecutivos falharem o nó é removido da lista. O health-check é feito a cada 5 segundos e consiste em verificar se o nó está no endereço fornecido.

### Falhas

O sistema é capaz de se recuperar de falhas de nós e de blocos. Se um nó falhar ele é removido da lista e os outros nós continuam funcionando normalmente. Se um bloco for invalido ele não é adicionado na lista assim mantendo a integridade da lista.

## Pontos de melhoria

- Adicionar um sistema de consenso para garantir que todos os nós tenham a mesma lista (Pode ser feito com transações distribuídas).
- Adicionar um sistema de consenso para garantir um mesmo grupo de nós.

## Referências

- FastAPI: <https://fastapi.tiangolo.com/>
- Requests: <https://docs.python-requests.org/en/latest/>
- Rocketry: <https://rocketry.readthedocs.io/en/stable/>
- SQLite: <https://docs.python.org/3/library/sqlite3.html>
- SqlAlchemy: <https://www.sqlalchemy.org/>
- Pydantic: <https://pydantic-docs.helpmanual.io/>
- Poetry: <https://python-poetry.org/>
