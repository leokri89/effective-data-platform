FROM jenkins/jenkins:lts-jdk11
# if we want to install via apt
USER root
#RUN  apt-get install -y ruby make more-thing-here
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

WORKDIR /opt

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && pip3.9 install virtualenv && pip3.9 install pytest

USER jenkins