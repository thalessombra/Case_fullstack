FROM node:20-alpine AS runner
WORKDIR /app


COPY package.json ./ 
COPY package-lock.json ./ 
COPY .next ./.next
COPY public ./public

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]  # ou ["npm", "run", "start"] dependendo do seu package.json
