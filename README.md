# 🧪 Teste Manager

Este projeto é um sistema simples de gerenciamento com funcionalidades voltadas para **usuários**, **produtos** e **faturamento**. Desenvolvido em Python, ele utiliza um banco de dados SQLite para armazenamento local.

## 📦 Estrutura do Projeto

├── main.py
├── database.py
├── billing_interface.py
├── product_interface.py
├── user_interface.py
├── menu_interface.py
├── requirements.txt
└── users.db


### 🔹 `main.py`
Arquivo principal do projeto. Ele serve como ponto de entrada do sistema. Provavelmente contém o menu inicial e a lógica que conecta os diferentes módulos/interfaces.

---

### 🔹 `database.py`
Responsável por toda a lógica de conexão com o banco de dados (`users.db`), criação de tabelas e execução de consultas (inserção, busca, atualização, exclusão).

**Funções comuns esperadas:**
- Conectar ao banco SQLite
- Criar tabelas (usuários, produtos, etc.)
- Funções genéricas de CRUD

---

### 🔹 `user_interface.py`
Gerencia todas as ações relacionadas aos **usuários** do sistema.

**Funcionalidades esperadas:**
- Cadastro de usuário
- Listagem de usuários
- Busca de usuário por ID ou nome
- Edição e remoção de usuários

---

### 🔹 `product_interface.py`
Controla as operações com **produtos**, como cadastro, listagem, edição e exclusão.

**Funcionalidades esperadas:**
- Adicionar novos produtos
- Listar produtos disponíveis
- Atualizar informações de produtos
- Remover produtos

---

### 🔹 `billing_interface.py`
Módulo relacionado ao **faturamento e cobranças**.

**Possíveis funções:**
- Registrar vendas ou transações
- Calcular totais
- Gerar comprovantes ou relatórios de faturamento

---

### 🔹 `menu_interface.py`
Responsável por apresentar menus ao usuário e organizar a navegação entre as opções do sistema. É aqui que o usuário escolhe se quer gerenciar usuários, produtos ou ver informações de faturamento.

---

### 🔹 `requirements.txt`

- Lista de dependências utilizadas no projeto (por padrão, pode estar vazio se o projeto usa apenas a biblioteca padrão do Python).

---

### 🔹 `users.db`

- Arquivo do banco de dados SQLite, gerado automaticamente após a execução do sistema.

---

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/caiionog/teste_manager.git
   cd teste_manager

📌 Melhorias Futuras
    
- Interface gráfica (Tkinter ou PyQt).

- Exportação de relatórios.

- Autenticação de usuários.

- Logs de operação.


- Desenvolvido por Caio Nogueira e João Victor Braga.
- GitHub: @caiionog




---
