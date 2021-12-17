#!/bin/sh

/usr/sbin/rsyslogd &
/usr/sbin/slapd -h "ldap:///" &
/usr/bin/tail -f /var/log/openldap/openldap.log
