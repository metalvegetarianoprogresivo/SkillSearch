FROM node:latest

# Install dependencies from package.json file
COPY package.json ./
RUN npm install

# Copy files and set the working directory
RUN mkdir /fake_server
COPY . ./fake_server
WORKDIR /fake_server

# Run the fake server
CMD ["npm", "start"]
