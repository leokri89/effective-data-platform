docker build -t krakenservices:v0.1.0 --file KrakendSimple.Dockerfile .

#Build para a versao flexivel
#docker build --build-arg ENV=dev -t krakenservices .