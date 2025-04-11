FROM node:lts-alpine as build-stage

# Create app directory and change ownership
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

# Copy package files as root and change ownership
COPY package*.json ./
RUN chown node:node package*.json

# Switch to the node user
USER node

# Install dependencies
RUN npm install

# Copy all application files and change ownership
COPY --chown=node . .

# Build the application
RUN npm run build

FROM nginx:stable-alpine as production-stage

# Copy built files to nginx directory
COPY --from=build-stage /home/node/app/dist /usr/share/nginx/html

# Expose the port
EXPOSE 8000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]