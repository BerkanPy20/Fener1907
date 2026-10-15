docker system prune
docker image prune --all

#launch container
docker compose -f ./docker-compose-jetson-setup.yml up --detach 

#pull embedding model
curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "bge-m3", "stream": false}'

docker compose -f ./docker-compose-jetson-setup.yml down