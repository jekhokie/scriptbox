FROM alpine

RUN apk add bind~9.16

RUN mkdir -p /etc/bind && chown root:named /etc/bind/ && chmod 755 /etc/bind && \
    mkdir -p /var/cache/bind && chown named:named /var/cache/bind && chmod 755 /var/cache/bind && \
    mkdir -p /var/lib/bind && chown named:named /var/lib/bind && chmod 755 /var/lib/bind && \
    mkdir -p /var/log/bind && chown named:named /var/log/bind && chmod 755 /var/log/bind && \
    mkdir -p /run/named && chown named:named /run/named && chmod 755 /run/named && \
    touch /var/log/bind/bind.log && chown named:named /var/log/bind/bind.log && chmod 755 /var/log/bind/bind.log

COPY files/named.conf /etc/bind/named.conf
COPY files/db.mytest.com /etc/bind/db.mytest.com

VOLUME ["/etc/bind", "/var/log"]

EXPOSE 53/udp

CMD /usr/sbin/named -c /etc/bind/named.conf -u named & /usr/bin/tail -f /var/log/bind/bind.log
