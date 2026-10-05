#!/bin/bash
# Provision the domain on first start, then run Samba as a domain controller.
set -e

if [ ! -f /var/lib/samba/private/sam.ldb ]; then
    echo "Provisioning domain $REALM ..."
    samba-tool domain provision \
        --realm="$REALM" --domain="$DOMAIN" --server-role=dc \
        --dns-backend=SAMBA_INTERNAL --adminpass="$LAB_PASSWORD" \
        --host-name=dc1 --use-rfc2307 >/var/log/provision.log 2>&1
    cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
    seed.sh >/var/log/seed.log 2>&1
fi

# The domain controller is its own DNS server, as in a real domain.
echo "nameserver 127.0.0.1" > /etc/resolv.conf
cp /etc/resolv.conf /etc/resolv.conf.good

echo "Domain controller starting. Open a shell with: docker compose exec dc bash"
exec samba --foreground --no-process-group
