# Step 1: Use an official Node.js image to build the React app
FROM node:18-alpine AS build

# Step 2: Set the working directory inside the container
WORKDIR /usr/src/app

# Step 3: Copy the package.json from the app directory to install dependencies
COPY app/package*.json ./

# Step 4: Install the dependencies
RUN npm install

# Step 5: Copy the rest of the app's code
COPY app ./app

# Step 6: Build the React app for production
RUN npm run build --prefix app

# Step 7: Use an NGINX image to serve the build
FROM nginx:1.23-alpine

# Step 8: Copy the build files from the Node.js build stage to the NGINX container
COPY --from=build /usr/src/app/app/build /usr/share/nginx/html

# Step 9: Expose port 80 for NGINX
EXPOSE 80

# Step 10: Start the NGINX server
CMD ["nginx", "-g", "daemon off;"]
