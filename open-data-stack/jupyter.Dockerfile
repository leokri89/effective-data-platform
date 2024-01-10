FROM repo.intranet.pags/base-images/python:3.9-centos7

RUN yum-config-manager --save --setopt=epel.sslverify=false && yum -y install java-11-openjdk-devel curl

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt

RUN rm /usr/bin/python && ln -s /usr/local/bin/python3.9 /usr/bin/python

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

RUN mkdir -p /opt/flink/jars

RUN curl -o /opt/flink/jars/flink-sql-connector-kafka-3.0.2-1.18.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar

RUN mkdir /notebooks

RUN groupadd --gid 65001 notebookuser && useradd --uid 65001 --gid 65001 notebookuser

RUN chown -R notebookuser /notebooks/ && \
chmod -R 700 /notebooks && \
chown -R notebookuser /opt/flink/jars/ && \
chmod -R 700 /opt/flink/jars && \
chown -R notebookuser /usr/local/lib/python3.9/site-packages/pyflink/log/ && \
chmod -R 700 /usr/local/lib/python3.9/site-packages/pyflink/log

USER 65001

RUN jupyter notebook --generate-config

COPY /conf/jupyter_notebook_config.py /home/notebookuser/.jupyter/jupyter_notebook_config.py

ENTRYPOINT [ "jupyter", "lab"]