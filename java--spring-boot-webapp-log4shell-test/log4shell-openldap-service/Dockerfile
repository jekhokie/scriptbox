FROM alpine

RUN apk add openldap openldap-clients openldap-back-mdb rsyslog tini
RUN mkdir -p /run/openldap && chown ldap:ldap /run/openldap && chmod 750 /run/openldap && \
    mkdir -p /var/log/openldap && chown ldap:ldap /var/log/openldap && chmod 755 /var/log/openldap && \
    touch /var/log/openldap/openldap.log && chown ldap:ldap /var/log/openldap/openldap.log && chmod 755 /var/log/openldap/openldap.log && \
    sed -i 's/module(load="imklog")//' /etc/rsyslog.conf && \
    echo "local4.* /var/log/openldap/openldap.log" >> /etc/rsyslog.conf

COPY files/base.ldif /etc/openldap/base.ldif
COPY files/slapd.conf /etc/openldap/slapd.conf
COPY files/entrypoint.sh /entrypoint.sh

RUN chmod 775 /entrypoint.sh
# query password for root user is "test"
RUN slapadd -c -l /etc/openldap/base.ldif -n1

# to test running instance:
#   ldapsearch -x -b 'dc=example,dc=com' '(objectclass=*)'

EXPOSE 389/tcp

ENTRYPOINT ["/sbin/tini", "-v", "-g", "--", "/entrypoint.sh"]
