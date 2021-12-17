# Spring Boot Webapp Log4Shell Test

Java spring boot application framework that allows testing the variants of the log4j vulnerabilities that
popped up in December of 2021. Specifically, has testing for (see details below):

- [CVE-2021-4104](https://nvd.nist.gov/vuln/detail/CVE-2021-4104): JMSAppender in Log4j 1.2 is vulnerable to
deserialization of untrusted data when the attacker has write access to the Log4j configuration.
- [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228): Apache Log4j2 2.0-beta9 through 2.12.1 and
2.13.0 through 2.15.0 JNDI features used in configuration, log messages, and parameters do not protect against
attacker controlled LDAP and other JNDI related endpoints.
- [CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046): It was found that the fix to address
CVE-2021-44228 in Apache Log4j 2.15.0 was incomplete in certain non-default configurations.

## Warning

This repository attempts to configure and run multiple known vulnerable versions of the log4j library. Do
*NOT* attempt to run this on any production system you intend to protect - it is intended for educational
purposes only.

## Getting Started

First, build the various Docker images required for the scenario testing:

```bash
$ ./build_images.sh
# will sequentially build all required docker images
```

Then, launch them using Docker/docker-compose!

```bash
$ docker-compose up
```

At this point, you should have all containers running in order to execute any/all tests below.

## Specific Testing/Use Cases

The below details the various tests that can be performed to demonstrate exploiting a vulnerable Java
application running a version of the log4j package susceptible to the various CVEs listed. Using the below exploit
techniques, attempt these against any of the below use cases/containers to prove whether the exploit is resolved in
the particular running container or not.

TODO: HOW TO EXPLOIT

### log4j 2.8.2 Vulnerable

Base container that runs the 2.8.2 version of log4j without any mitigation/remediation in place (for pentesting).
Port: 8880

### log4j 1.2 JMSAppender Exploit

log4shell-app-1.2-jmsAppender-mitigated
[Remove JMSAppender Class Mitigation](https://access.redhat.com/security/cve/CVE-2021-4104#cve-details-mitigation)
Port: 8881

### log4j 2.8.2 formatMsgNoLookups=true

log4shell-app-2.8.2-formatMsgNoLookups-mitigated
[formatMsgNoLookups=true Mitigation](https://www.lunasec.io/docs/blog/log4j-zero-day-mitigation-guide/#option-2-enable-formatmsgnolookups)
Port: 8882

### log4j 2.8.2 JNDI Lookup Patch

log4shell-app-2.8.2-jndiLookupRemoved-mitigated
[Remove JNDI Lookups Class Mitigation](https://www.lunasec.io/docs/blog/log4j-zero-day-mitigation-guide/#option-3-jndi-patch)
Port: 8883

### log4j 2.8.2 {nolookups}

log4shell-app-2.8.2-nolookups-mitigated
[Add nolookups to XML Mitigation](https://www.lunasec.io/docs/blog/log4j-zero-day-mitigation-guide/#option-3-jndi-patch)
Port: 8884

### log4j 2.16.0 Remediation

**RECOMMENDED** - permanent fix

log4shell-app-2.16.0-remediated
[Upgrading to 2.16 Remediation](https://www.lunasec.io/docs/blog/log4j-zero-day-mitigation-guide/#option-1-upgrading-to-2160)
Port: 8885
