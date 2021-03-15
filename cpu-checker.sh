#!/usr/bin/env bash
tmpfile=$1

while [ -f $tmpfile ];
do
    ssh centos113 "sleep 1; top -p \$(/usr/sbin/pidof mysqld) -b -n1"|grep '%CPU' -A1|awk 'NR>1{print $9}' >> $tmpfile
done
