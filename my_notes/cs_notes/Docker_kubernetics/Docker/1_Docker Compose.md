# start mongodb docker run command

docker run -d \
-p 27017:27017 \
-e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
-e ME_CONFIG_MONGODB_ADMINPASSWORD=admin \
--network mongo-network \
--name mongodb \
mongo


docker run -d \
-p 8081:8081 \
-e me_config_mongodb_adminusername=admin \
-e me_config_mongodb_adminpassword=admin \
--network mongo-network \
--name mongo-express \
mongo-express


# Start mongodb docker compose 
# compose.yaml

version: '3.1'
services:
  mongodb: #container_name 
    image: mongo  #image_want_to_pull
    ports:
      - 27017:27017 #host : #container
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin  

  mongo-express: #container-name
    image: mongo-express
    ports: 
      - 8081:8081
    environment: #environment_variables
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin 
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin


