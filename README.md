# 📈 Case Fullstack

Projeto fullstack para gerenciamento e visualização de ativos financeiros, contendo **frontend** em Next.js e **backend** com API em Python/Django (rodando via Docker).

---

## 📂 Estrutura do Projeto

---

## 🚀 Tecnologias Utilizadas

## **Frontend**

- [Next.js](https://nextjs.org/) 15+
- [React](https://react.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- [Shadcn/UI](https://ui.shadcn.com/)

## **Backend**

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)

## **Outros**

- Docker & Docker Compose
- TypeScript
- Python 3.12+

---

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado na sua máquina:

- [Node.js 20+](https://nodejs.org/)
- [npm](https://www.npmjs.com/) ou [pnpm](https://pnpm.io/)
- [Docker](https://www.docker.com/)

---

## 🖥️ Como rodar o projeto

### **1. Clonar o repositório**

```bash```
git clone [text](https://github.com/thalessombra/Case_fullstack)
cd Case_fullstack

## 2. Rodando o backend com Docker

No diretório raiz do projeto, execute:
```bash```
docker compose up --build
A API ficará disponível em:

<http://localhost:8000>

📜 3. Aplicando migrations no backend

Após os containers subirem, rode:

docker compose exec backend python manage.py migrate

🌱 4. Rodando seeds (dados iniciais)

Se existir um comando de seed configurado:

docker compose exec backend python manage.py loaddata seed.json

(ou o comando que você usa para popular os dados iniciais)

💻 5. Rodando o frontend localmente

Entre na pasta frontend:

cd frontend
npm install

Rode o servidor de desenvolvimento:

npm run dev

O app ficará disponível em:

<http://localhost:3000>

📌 Observações importantes

O backend é totalmente gerenciado pelo Docker, então não precisa instalar Python ou Postgres localmente.

Caso altere variáveis de ambiente, reinicie os containers:

docker compose down && docker compose up --build

O frontend acessa a API via URL configurada no .env.local.

🔑 Exemplo de .env.local (frontend)

Crie um arquivo .env.local na pasta frontend:

NEXT_PUBLIC_API_URL=<http://localhost:8000>

🛠️ Scripts úteis

Frontend

npm run dev     # roda em modo desenvolvimento
npm run build   # build de produção
npm start       # inicia o servidor em produção

Backend (via Docker)

docker compose up --build
docker compose down
docker compose logs -f
docker compose exec backend python manage.py migrate  
docker compose exec backend python manage.py createsuperuser  
docker compose exec backend python manage.py loaddata seed.json
