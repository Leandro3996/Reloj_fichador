#!/bin/bash
echo "Parando contenedores..."
docker-compose down
echo "Iniciando contenedores..."
docker-compose up -d
