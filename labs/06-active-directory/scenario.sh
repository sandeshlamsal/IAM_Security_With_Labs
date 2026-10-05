#!/bin/bash
# Break something on purpose, so you can practise diagnosing it.
#   scenario.sh 1..6   introduce a fault and print only the symptom
#   scenario.sh reset  put everything back
P="$LAB_PASSWORD"

reset() {
    cp /etc/resolv.conf.good /etc/resolv.conf
    for u in priya tom asha lena svc-web; do
        samba-tool user enable "$u" >/dev/null 2>&1
        samba-tool user unlock "$u" >/dev/null 2>&1
        samba-tool user setpassword "$u" --newpassword="$P" >/dev/null 2>&1
        samba-tool user setexpiry "$u" --noexpiry >/dev/null 2>&1
    done
    samba-tool spn delete HTTP/intranet.lab.example.com >/dev/null 2>&1
    kdestroy -q 2>/dev/null
    echo "Lab reset."
}

case "$1" in
1)  echo "nameserver 192.0.2.53" > /etc/resolv.conf
    echo "Symptom: nobody on this machine can log on. Try: kinit priya" ;;
2)  for i in 1 2 3 4; do echo "wrong-password" | kinit tom >/dev/null 2>&1; done
    echo "Symptom: Tom says his password stopped working. Try: kinit tom" ;;
3)  samba-tool user disable asha >/dev/null
    echo "Symptom: Asha cannot log on. Try: kinit asha" ;;
4)  samba-tool user setpassword lena --newpassword="$P" --must-change-at-next-login >/dev/null
    echo "Symptom: Lena cannot get into the application. Try: kinit lena" ;;
5)  samba-tool spn delete HTTP/intranet.lab.example.com >/dev/null 2>&1
    echo "Symptom: the intranet keeps prompting for credentials."
    echo "Try: kinit priya, then: kvno HTTP/intranet.lab.example.com" ;;
6)  samba-tool user setexpiry svc-web --days=-1 >/dev/null 2>&1 || samba-tool user setexpiry svc-web --days=0 >/dev/null
    echo "Symptom: the web application's service stopped authenticating overnight. Try: kinit svc-web" ;;
reset) reset ;;
*)  echo "Usage: scenario.sh 1|2|3|4|5|6|reset" ;;
esac
