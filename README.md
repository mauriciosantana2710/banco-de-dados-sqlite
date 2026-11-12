# Cadastro de Produtos (Python + SQLite)

Pequeno sistema desktop para cadastro de produtos, feito com **Python**, **Tkinter** e **SQLite** (via `pyodbc`). Tem tela de login e um CRUD simples de produtos.

## Funcionalidades

- **Login** com usuário e senha validados no banco (tecla Enter também entra; botão para mostrar/ocultar a senha).
- **Listagem** dos produtos em uma tabela com linhas alternadas e barra de rolagem.
- **Pesquisar por nome**: filtra a tabela enquanto você digita.
- **Cadastrar** novo produto (nome, descrição e preço).
- **Editar** um produto com duplo clique na linha.
- **Deletar** produtos, com confirmação, pela tela principal ou pela janela de edição.

## Requisitos

- Python 3.8+ (o Tkinter já vem com a instalação padrão no Windows)
- [`pyodbc`](https://pypi.org/project/pyodbc/)
- [SQLite3 ODBC Driver](http://www.ch-werner.de/sqliteodbc/) instalado (o driver precisa ter o mesmo nome usado no código: `SQLite3 ODBC Driver`)

```bash
pip install pyodbc
```

## Banco de dados

O programa espera um arquivo `Projeto_Compras.db` na mesma pasta do script, com duas tabelas:

```sql
CREATE TABLE Usuarios (
    Usuario TEXT NOT NULL,
    Senha   TEXT NOT NULL
);

CREATE TABLE Produtos (
    ID        INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome      TEXT,
    Descricao TEXT,
    Preco     REAL
);

-- usuário de exemplo
INSERT INTO Usuarios (Usuario, Senha) VALUES ('admin', '1234');
```

> A ordem das colunas de `Produtos` importa: ID, Nome, Descrição, Preço.

## Como executar

```bash
python "cadastro_de_produtos.py"
```

Entre com um usuário cadastrado na tabela `Usuarios`. A tela de produtos abre em seguida.

## Observações

- Projeto de estudo: as senhas são salvas e comparadas em texto puro, sem criptografia. Não use em produção.
- O preço ainda não é validado (aceita qualquer texto).

## Tecnologias

Python · Tkinter / ttk · SQLite · pyodbc
