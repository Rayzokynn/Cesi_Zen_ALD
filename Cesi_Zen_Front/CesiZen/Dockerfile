FROM node:lts-slim
# Set the working directory in the container 
WORKDIR /app
# Install system dependencies and clean up apt cache
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
# Install Ionic CLI globally
RUN npm install -g @ionic/cli
# Copy package.json and package-lock.json to the container and install dependencies
COPY package*.json ./
# Install project dependencies
RUN npm install 
# Copy the entire project into the container
COPY . .
# Expose the port that the Ionic development server will run on
EXPOSE 8100
# Run the Ionic development server
CMD ["ionic", "serve", "--external", "--port", "8100"]
