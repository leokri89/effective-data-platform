set IMG_NAME=dax-tools-app
set IMG_VERSION=0.3.0

docker build -t %IMG_NAME%:%IMG_VERSION% .

docker tag %IMG_NAME%:%IMG_VERSION% repo.intranet.pags/dataplatform-docker-dev-local/data-analytics/valinor/%IMG_NAME%:%IMG_VERSION%
docker push repo.intranet.pags/dataplatform-docker-dev-local/data-analytics/valinor/%IMG_NAME%:%IMG_VERSION%

kubectl config use-context kubernetes-dev-tb
kubectl apply -f deploy/dev/deployment_gt.yml
kubectl apply -f deploy/dev/service_gt.yml
kubectl apply -f deploy/dev/ingress_gt.yml