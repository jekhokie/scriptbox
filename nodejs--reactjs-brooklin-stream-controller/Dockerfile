FROM openjdk:8u212-jre-alpine

ENV BROOKLIN_FILENAME=brooklin-1.1.0.tgz \
    BROOKLIN_HOME=/opt/brooklin-1.1.0

RUN apk add bash \
    && wget https://github.com/linkedin/brooklin/releases/download/1.1.0/${BROOKLIN_FILENAME} -O /tmp/${BROOKLIN_FILENAME} \
    && tar -xzvf /tmp/${BROOKLIN_FILENAME} -C /opt/ \
    && rm /tmp/${BROOKLIN_FILENAME}

COPY brooklin-config/server.properties ${BROOKLIN_HOME}/config/server.properties

CMD /bin/bash ${BROOKLIN_HOME}/bin/brooklin-server-start.sh ${BROOKLIN_HOME}/config/server.properties 2>&1
