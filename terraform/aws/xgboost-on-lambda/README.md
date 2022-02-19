
**Como usar:**
Acesse a EC2 criada pelo terraform na raiz desse diretorio e execute os comando abaixo para criar um pacote com as bibliotecas e copia-las para o EFS

### **Configuração das Bibliotecas**
#### **Versão 1**
```bash
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


## << TREINE O MODELO E SALVE COMO PICKLE >> ##


cp model_pickle.pkl /mnt/efs/efs/
```

#### **Versão 2**
```bash
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

mkdir -p ./src/package
cd ./src

pip install --target ./package numpy scipy xgboost joblib

cp -r ./package/* /mnt/efs/efs/package/


## << TREINE O MODELO E SALVE COMO PICKLE >> ##


cp model_pickle.pkl /mnt/efs/efs/
```