FROM jenkins/jenkins:lts-jdk11
# if we want to install via apt
USER root

RUN apt-get update && apt-get install -y lsb-release

RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg

RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

RUN apt-get update && apt-get install -y docker-ce-cli

RUN apt-get update && \
apt install -y build-essential \
zlib1g-dev \
libncurses5-dev \
libgdbm-dev \
libnss3-dev \
libssl-dev \
libsqlite3-dev \
libreadline-dev \
libffi-dev \
curl \
libbz2-dev \
wget

WORKDIR /opt

RUN wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz \
&& tar -xf Python-3.9.1.tgz \
&& mv /opt/Python-3.9.1 /opt/Python39 \
&& chmod 777 -R Python39

WORKDIR /opt/Python39

RUN ./configure --enable-optimizations && make -j 2 && make altinstall && python3.9 --version

ENV PATH="/opt/Python39:${PATH}"

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

USER jenkins

RUN jenkins-plugin-cli --plugins "blueocean:1.26.0 docker-workflow:563.vd5d2e5c4007f"