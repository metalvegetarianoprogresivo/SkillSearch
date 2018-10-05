FROM node:latest

# Install json-server library in global mode
RUN npm install -g json-server

# Setup the working directory
COPY . /data
WORKDIR /data

# Install the fake server application from the package.json file
RUN npm install

# Run the fake server
CMD ["node", "test_server.js"]
