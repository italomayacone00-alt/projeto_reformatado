# Sistema de Gerenciamento de Estoque, Pedidos e Clientes

> **Resumo:** Projeto web completo para gestão de clientes, produtos/estoque e pedidos, criado como projeto de portfólio colaborativo entre um estudante de Ciência da Computação (desenvolvimento backend) e um Engenheiro de Produção (regras e operações de estoque). O objetivo é demonstrar boas práticas de engenharia de software, arquitetura organizada, testes automatizados e aplicações reais de métodos de engenharia de produção (ABC, PEPS, endereçamento de prateleiras).

---

## Links rápidos
- Demo (local): `http://localhost:8000`
- Docs da API (Swagger): `/apidocs`
- Status: Em desenvolvimento

## Como rodar (PowerShell)

Siga estes passos no **PowerShell** (Windows) a partir da raiz do projeto:

```powershell
cd "c:\Users\italo\OneDrive\Área de Trabalho\projeto_reformatado"
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requeriments.txt
# Opcional: crie um arquivo .env na raiz com SECRET_KEY e DATABASE_URL
python app\app.py
```

Observações rápidas:
- O `Config` já contém fallback para `sqlite:///site.db` se `DATABASE_URL` não for definido.
- `app/app.py` executa `db.create_all()` no contexto da app, então as tabelas serão criadas automaticamente na primeira execução.
- Em produção, use um servidor WSGI (ex.: `waitress`) e desative `debug=True`.

---

## Tecnologias
- **Linguagem:** Python 3.12+
- **Framework Backend:** Flask
- **Banco de Dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **ORM / Migrações:** SQLAlchemy + Alembic
- **Autenticação:** JWT + Flask-Login
- **Frontend:** Bootstrap 5 + Vanilla JS / jQuery
- **Testes:** PyTest
- **Documentação da API:** Swagger (Flasgger)
- **Containerização / Orquestração:** Docker + Docker Compose

---

## Objetivos do projeto (visão do portfólio)
Este repositório foi criado para que recrutadores vejam:
- Arquitetura limpa (separação de camadas: models, repositories, services, routes).
- Testes automatizados cobrindo regras de negócio e endpoints críticos.
- Integração de requisitos de Engenharia de Produção (políticas ABC, PEPS, endereçamento de estoque).
- Implantação via Docker (facilidade de replicação do ambiente).
- Documentação clara (README, Swagger, exemplos de uso).

---

## Principais funcionalidades
### Módulos
- **Clientes:** CRUD completo, validação de CPF/CNPJ (único) e regras de negócio (ex.: exclusão apenas sem pedidos ativos).
- **Produtos / Estoque:** cadastro de produtos com lote, validade, dimensões, peso, endereço físico (corredor → prateleira → nível), entradas e saídas.
- **Pedidos:** criação, alteração de status (Em aberto → Pago → Enviado → Concluído | Cancelado), cálculo automático do valor total, impacto no estoque (reserva e débito), reversão no cancelamento.
- **Relatórios:** vendas, movimentações, ocupação de prateleiras, alertas de validade.
- **Módulo de Qualidade:** ferramentas para Pareto, Ishikawa, checklists e PDCA simplificado.

---

## Regras de domínio (resumo técnico)
- CPF/CNPJ único por cliente; e-mail opcional mas validado quando presente.
- Quantidades não podem ser negativas; entradas aumentam estoque, confirmações diminuem.
- PEPS obrigatório para perecíveis; produtos com validade próxima possuem prioridade de saída.
- Classificação ABC por giro para alocação de prateleiras.
- Itens pesados/volumosos respeitam restrições de alocação física.
- Pedido só pode ser confirmado com ao menos um produto válido.
- Cancelamento reverte movimentações de estoque.

---

## Estrutura do repositório
```
project/
│── app/
│   ├── models/        # Modelos SQLAlchemy (Client, Product, StockLocation, InventoryMovement, Order, OrderItem, etc.)
│   ├── routes/        # Blueprints por módulo
│   ├── services/      # Regras de negócio (ex.: checkout, alocação, movimentos)
│   ├── repositories/  # Acesso ao DB, queries complexas
│   ├── templates/     # Páginas HTML (Bootstrap)
│   ├── static/        # CSS, JS, assets
│   └── utils/         # Helpers: validação de CPF/CNPJ, JWT, utils de data
│
│── tests/             # Testes unitários e integração (PyTest)
│── migrations/        # Alembic
│── config.py          # Configurações por ambiente
│── requirements.txt
│── docker-compose.yml
│── Dockerfile
│── run.py
```

---

## Modelagem (visão geral)
- **Client**: id, nome, cpf_cnpj, email, phone, endereço
- **Product**: id, sku, nome, descrição, peso, dimensões, classe_abc, perecível(boolean)
- **StockLocation**: id, corredor, prateleira, nível, capacidade (peso/volume)
- **InventoryBatch**: id, product_id, lote, data_validade, quantidade
- **InventoryMovement**: id, batch_id, tipo (entrada/saida/reserva), quantidade, documento (pedido_id)
- **Order**: id, client_id, status, total, created_at
- **OrderItem**: id, order_id, product_id, quantidade, unit_price, batch_allocated

(Adicionar diagrama ER no diretório `docs/` se desejar)

---

## Scripts úteis / comandos
### Setup local (com Docker)
```bash
# build e start
docker-compose up --build -d

# rodar migrations
docker-compose exec web alembic upgrade head

# criar dados de amostra
docker-compose exec web python manage.py seed_data
```

### Setup sem Docker (ambiente dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# ajustar vars de DB
flask db upgrade
flask run --host 0.0.0.0 --port 8000
```

---

## Variáveis de ambiente (exemplo `.env.example`)
```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=trocar_para_uma_chave_segura
DATABASE_URL=sqlite:///dev.db  # ou postgres://user:pass@host:port/dbname
JWT_SECRET=trocar_para_uma_chave_jwt
```

---

## Testes e qualidade
- Executar testes: `pytest --maxfail=1 --disable-warnings -q`
- Cobertura mínima alvo: **70%** (meta do projeto)
- Ferramentas sugeridas: `flake8`, `isort`, `black` (formatação), `pre-commit` hooks

---

## Endpoints principais (exemplos)
- `POST /auth/login` → autenticação (JWT)
- `POST /clients` → criar cliente
- `GET /clients/{id}` → obter cliente
- `POST /products` → criar produto
- `POST /inventory/entries` → registrar entrada de estoque (lote)
- `POST /orders` → criar pedido (reserva e cálculo)
- `PATCH /orders/{id}/confirm` → confirmar pedido (debita estoque)
- `PATCH /orders/{id}/cancel` → cancelar pedido (reverte movimentações)
- `GET /reports/movements` → relatórios de movimentação
- `GET /reports/occupancy` → ocupação por corredor/prateleira

---

## Como apresentar este projeto em entrevistas (dica para recrutadores)
- Explique a **separação de responsabilidades** (models, repositories, services) e por que isso facilita manutenção e testes.
- Mostre os **testes que cobrem regras de negócio** mais complexas (ex.: alocação PEPS, cancelamento de pedido que reverte estoque).
- Demonstre a **colaboração com o Engenheiro de Produção**: como os requisitos de logística (endereçamento, capacidade, políticas ABC/PEPS) influenciaram as decisões de modelagem e UI.
- Aponte o uso de **conteinerização** e como isso facilita replicar o ambiente do avaliador.

---

## O que cada membro da dupla entregou (para README do portfólio)
- **Estudante de Ciência da Computação (Desenvolvedor Backend):** arquitetura do backend, implementação de endpoints REST, autenticação JWT, testes automatizados, Docker, integração com Alembic/SQLAlchemy e documentação da API.
- **Engenheiro de Produção:** definição das regras de domínio de estoque (endereçamento, ABC, PEPS), métricas de ocupação e recomendações operacionais, checklists de qualidade e fluxos de inventário cíclico.

---

## Próximos passos / melhorias planejadas
- Integração com gateways de pagamento e emissão de NF-e.
- Dashboard analítico e exportação de relatórios (CSV / XLSX).
- Implementar filas (RabbitMQ / Celery) para processamento assíncrono de tarefas (ex.: geração de relatórios, notificações de vencimento).
- Monitoramento e CI/CD (ex.: GitHub Actions → deploy automático em staging).

---

## Como contribuir
1. Fork no repositório
2. Criar branch `feature/<nome>`
3. Abrir PR descrevendo mudanças e test coverage
4. Código deve seguir `black` + `flake8`

---

## Contato
- **Desenvolvedor (Ciência da Computação):** `igorzon` (GitHub) — *link no perfil do repositório*
- **Engenheiro de Produção:** `nome_do_amigo` — *incluir LinkedIn ou contato profissional*

---

## Licença
Escolha uma licença (ex.: MIT) e adicione o arquivo `LICENSE`.

---

> Se quiser, eu posso também gerar automaticamente:
> - um `docker-compose.yml` de exemplo;
> - modelos de migrations e seeds;
> - exemplos de testes PyTest cobrindo PEPS/ABC e o fluxo de pedido.



