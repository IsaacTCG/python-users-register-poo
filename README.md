# Python: Runtime User Register

Cadastro de usuários em memória feito com Python puro.

O objetivo deste projeto é praticar fundamentos da linguagem Python somente utilizando bibliotecas nativas quando necessário, sem frameworks, sem banco de dados ou arquitetura complexa. Os dados ficam salvos apenas em cache runtime, ou seja, existem somente enquanto o programa está em execução.

## Como usar

Execute o arquivo principal:

```bash
python src/main.py
```

Requisitos:

- Python 3.10 ou superior

O projeto utiliza `match/case`, recurso disponível a partir do Python 3.10.

## Funcionalidades

- Listar usuários
- Buscar usuário por ID
- Criar usuário
- Atualizar usuário
- Remover usuário
- Paginar listagem
- Validar campos obrigatórios
- Validar e-mail duplicado
- Confirmar criação, atualização e remoção

## Menu

Ao iniciar o programa, será exibido o menu principal:

```text
----- Main Menu -----
1: Exit
2: List
```

Na listagem, é possível acessar as operações principais:

```text
1: Main Menu
2: Create
3: Find
4: Back Page
5: Next Page
```

A opção 3 só aparece quando há ao menos 1 usuário cadastrado.

As opções de paginação aparecem apenas quando existem usuários suficientes para mais de uma página.

## Estrutura dos dados

Os usuários são armazenados em um `dict`, usando o `id` como chave:

```python
users = {
    1: {
        "id": 1,
        "name": "JOHN DOE",
        "email": "JOHN.DOE@WHO.COM",
        "age": 100,
        "occupation": ""
    }
}
```

Essa escolha além de permitir buscar usuários por ID de forma direta, foi pensado na performance O(1):

```python
user = users.get(user_id)
```

## Cache runtime

O projeto não salva dados em arquivo nem em banco de dados.

Os usuários criados durante a execução ficam apenas em memória. Ao encerrar o programa, esses dados são perdidos.

Esse comportamento é intencional, pois o foco do projeto é praticar fundamentos do Python antes de evoluir para persistência, testes, orientação a objetos ou arquitetura em camadas.

## Validações

O sistema possui validações simples:

- Nome não pode ser vazio
- Nome não pode conter números
- E-mail não pode ser vazio
- E-mail precisa ter formato básico válido
- E-mail não pode ser duplicado
- Idade precisa ser um número inteiro
- Idade precisa ser maior ou igual a zero
- Ocupação pode ser vazia; nesse caso, recebe `UNKNOWN`

## Conceitos praticados

- Variáveis e constantes
- Funções
- Dicionários
- Loops com `while`
- Condicionais
- `match/case`
- `try/except`
- Entrada de dados com `input`
- Formatação com f-strings
- Paginação com slicing
- Organização básica de código

## Limitações

Este é um projeto de estudo. Por isso, ele ainda não possui:

- Persistência em arquivo
- Banco de dados
- Testes automatizados
- Separação em múltiplos arquivos
- Classes
- Framework web
- Arquitetura em camadas

## Próximos passos

Possíveis melhorias futuras:

- Separar o código em módulos e/ou classes
- Adicionar testes com `pytest`
- Usar `dataclass` e/ou `pydantic`
- Criar um repositório em memória
- Persistir dados em JSON
- Evoluir para uma API com FastAPI ou Django