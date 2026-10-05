# A Samba Active Directory domain controller for local practice. Lab use only.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      samba samba-ad-dc samba-ad-provision samba-dsdb-modules samba-vfs-modules winbind \
      krb5-user ldap-utils libsasl2-modules-gssapi-mit dnsutils openssl ca-certificates faketime \
 && rm -rf /var/lib/apt/lists/* /etc/samba/smb.conf
COPY entrypoint.sh seed.sh scenario.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/seed.sh /usr/local/bin/scenario.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
