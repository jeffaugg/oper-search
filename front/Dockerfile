# Etapa 1: build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

# Copia os arquivos necessários para instalar dependências
COPY package*.json ./
RUN npm install

# Copia o restante da aplicação
COPY . .

# Gera o build de produção
RUN npm run build

# Etapa 2: servir o build com nginx
FROM nginx:alpine

# Remove a config padrão e adiciona a nossa
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos do build para o nginx
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
