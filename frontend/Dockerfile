FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
RUN npm install -g serve
COPY --from=build /app/build /app/build
WORKDIR /app/build
EXPOSE 3000

CMD ["serve", "-s", "."]
    
# FROM node:18
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .

# # Build the app
# RUN npm run build

# # Output build contents for debugging
# RUN echo "Contents of build directory:" && ls -R build

# EXPOSE 3000

# # Use an environment variable to determine whether to run in dev or prod mode
# ENV NODE_ENV=production

# # Start the app based on NODE_ENV
# CMD if [ "$NODE_ENV" = "production" ] ; then \
#         npm install -g serve && serve -s build; \
#     else \
#         npm start; \
#     fi


# FROM node:18
#    WORKDIR /app
#    COPY package*.json ./
#    RUN npm install
#    COPY . .
#    RUN npm run build
#    RUN echo "Contents of build directory:" && ls -R build
#    EXPOSE 3000
#    CMD ["npm", "start"]