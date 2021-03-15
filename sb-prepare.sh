#!/bin/bash
 
host=192.168.99.113
#host192.168.10.110
port=$1
user='root'
password='chwing'
table_size=500000
rate=20
ps_mode='disable'
sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --threads=1 --max-requests=0 --time=3600 --mysql-host=$host --mysql-user=$user --mysql-password=$password --mysql-port=$port --tables=10 --report-interval=1 --skip-trx=on --table-size=$table_size --rate=$rate --db-ps-mode=$ps_mode prepare
