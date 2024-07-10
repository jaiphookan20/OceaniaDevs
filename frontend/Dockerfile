FROM node:14
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   RUN echo "Contents of build directory:" && ls -R build
   EXPOSE 3000
   CMD ["npm", "start"]