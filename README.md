# 📘 Projeto "Consulta de Operadoras de Saúde"

Este projeto realiza a importação e consulta de operadoras de planos de saúde com base em um arquivo CSV. Ele é dividido em dois módulos principais:

- **Back-end**: API REST em FastAPI que importa e serve os dados de operadoras de saúde.
- **Front-end**: Interface em Vue.js + Vite para busca interativa dessas operadoras.

---

## 🏗️ Estrutura do Projeto

```
oper-search/
├── back/                # API FastAPI
│   ├── app/             # Código fonte da API
│   ├── Dockerfile       # Docker da API
│   └── requirements.txt # Dependências Python
├── front/               # Front-end Vue 3 + Vite
│   ├── src/             # Componentes Vue
│   ├── nginx.conf       # Configuração NGINX
│   ├── Dockerfile       # Docker para build + NGINX
├── Index.csv            # Arquivo de dados de operadoras
└── docker-compose.yml   # Orquestração dos serviços
```

---

## ⚙️ Funcionalidades

- 🗂️ Importação de dados de um arquivo CSV.
- 🔍 Filtro por UF, cidade, modalidade, CNPJ e razão social.
- 🚀 Interface web amigável para busca.
- 🔧 API documentada automaticamente via Swagger.

---

## 📦 Backend (FastAPI + PostgreSQL)

### Principais arquivos:

- **`main.py`**: ponto de entrada da API, faz o startup e chama o importador.
- **`services/data_importer.py`**: importa os dados do CSV.
- **`routes/operadoras.py`**: endpoint `GET /api/v1/operadoras` com filtros.
- **`models/operadora.py`**: definição da tabela `operadoras` via SQLAlchemy.
- **`schemas/operadora.py`**: schemas de entrada/saída com Pydantic.

---

## 📡 API REST

### `GET /api/v1/operadoras`

| Parâmetro      | Tipo   | Descrição                                 |
|----------------|--------|-------------------------------------------|
| `uf`           | string | Unidade Federativa (ex: SP)               |
| `cidade`       | string | Cidade (parcial ou completa)              |
| `modalidade`   | string | Tipo de operadora                         |
| `cnpj`         | string | CNPJ exato                                |
| `razao_social` | string | Razão Social (parcial ou completa)        |
| `limit`        | int    | Número máximo de resultados (padrão: 100) |
| `offset`       | int    | Offset de paginação                       |

---

## 💻 Frontend (Vue.js + Vite)

### Funcionalidade:

- Formulário com campos de busca.
- Requisições à API via `fetch` com filtros.
- Renderização de resultados com Vue.

---

## 🐳 Docker

### 📁 `back/Dockerfile`

```dockerfile
FROM python:3.10-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### 📁 `front/Dockerfile` (Produção com build + nginx)

```dockerfile
# Etapa 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa 2: Servir com NGINX
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 📁 `front/nginx.conf`

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 📦 `docker-compose.yml`

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: fastapi
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: operadoras
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fastapi -d operadoras"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build:
      context: ./back
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://fastapi:secret@postgres:5432/operadoras
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./back/app:/app/app
      - ./Index.csv:/app/Index.csv

  front:
    build:
      context: ./front
    ports:
      - "8080:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## 🚀 Acesso à Aplicação

- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Comandos úteis

### Subir tudo:

```bash
docker-compose up --build
```

### Rebuild apenas do front:

```bash
docker-compose build front && docker-compose up front
```