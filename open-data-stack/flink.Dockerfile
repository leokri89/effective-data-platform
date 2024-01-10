FROM flink:1.18.0-scala_2.12

RUN curl -o /opt/flink/lib/flink-sql-connector-kafka-3.0.2-1.18.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar
RUN curl -o /opt/flink/lib/flink-sql-avro-confluent-registry-1.18.0.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.18.0/flink-sql-avro-confluent-registry-1.18.0.jar