FROM alpine

RUN apk add nginx php7 php7-fpm

RUN mkdir -p /var/log/nginx && chown root:root /var/log/nginx && chmod 755 /var/log/nginx && \
    touch /var/log/nginx/error.log && chown root:root /var/log/nginx/error.log && chmod 755 /var/log/nginx/error.log && \
    mkdir /www && chown nginx:nginx /www && \
    mkdir /bind9-logs && chown nginx:nginx /bind9-logs && chmod 640 /bind9-logs && \
    touch /www/favicon.ico && chown nginx:nginx /www/favicon.ico

COPY files/nginx.conf /etc/nginx/nginx.conf
COPY files/default.conf /etc/nginx/http.d/default.conf
COPY files/index.php /www/index.php

VOLUME ["/var/log"]

EXPOSE 80/tcp

CMD /usr/sbin/nginx -c /etc/nginx/nginx.conf & /usr/sbin/php-fpm7 & /usr/bin/tail -f /var/log/nginx/error.log
