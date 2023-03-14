set IMG_NAME=dax-docs
set IMG_VERSION=latest
set CONTAINER_NAME=dax-docs-container

echo "Criando imagem: %IMG_NAME%:%IMG_VERSION%"

docker rm -f %CONTAINER_NAME%
docker rmi -f %IMG_NAME%:%IMG_VERSION%
docker build -t %IMG_NAME%:%IMG_VERSION% -f Dockerfile .

docker run -d --rm -p 8000:8080 --name %CONTAINER_NAME% %IMG_NAME%:%IMG_VERSION%