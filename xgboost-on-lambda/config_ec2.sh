
sudo yum install amazon-efs-utils

cd /mnt

sudo mkdir efs

sudo mount -t efs -o tls fs-12345678:/ efs

sudo yum install atlas-devel \
    atlas-sse3-devel \
    blas-devel \
    findutils \
    gcc \
    gcc-c++ \
    lapack-devel \
    zip

python3 -m pip install --upgrade pip
python3 -m pip install numpy
python3 -m pip install scipy
python3 -m pip install xgboost
python3 -m pip install joblib

python3 -m site

cp -r site/* /mnt/efs/efs/site-package/

#################################
## ETAPA DE TREINAMENTO MODELO ##
#################################

cp model_pickle.pkl /mnt/efs/efs/
