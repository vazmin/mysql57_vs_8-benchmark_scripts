#!/usr/bin/env bash
 
host=192.168.99.113
port=$1
user="root"
password="chwing"
table_size=100000
tables=10
rate=20
ps_mode='disable'
threads=1
events=0
time=5
trx=100
path=$PWD
 
counter=1
 
echo "thread,cpu" > ${host}-cpu.csv
 
# for i in 16 32 64 128 256 512 1024 2048; 
for i in 16 32 64 128; 
do
 
    threads=$i
 
    mysql -u $user -P $port -h $host -p$password -e "SHOW GLOBAL STATUS" >> $host-$port-global-status.log
    tmpfile=$path/${host}-$port-tmp${threads}
    touch $tmpfile
    /bin/bash cpu-checker.sh $tmpfile $host $threads &
 
    /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --events=$events --threads=$threads --time=$time --mysql-host=$host --mysql-user=$user --mysql-password=$password --mysql-port=$port --report-interval=1 --skip-trx=on --tables=$tables --table-size=$table_size --rate=$rate --delete_inserts=$trx --order_ranges=$trx --range_selects=on --range-size=$trx --simple_ranges=$trx --db-ps-mode=$ps_mode --mysql-ignore-errors=all run | tee -a $host-$port-sysbench.log
 
    echo "${i},"`cat ${tmpfile} | sort -nr | head -1` >> ${host}-$port-cpu.csv
    unlink ${tmpfile}
 
    mysql -u $user -P $port -h $host -p$password -e "SHOW GLOBAL STATUS" >> $host-$port-global-status.log
done
 
python3 $path/innodb-ops-parser.py $host-$port
 
mysql -u $user -P $port -h $host -p$password -e "SHOW GLOBAL VARIABLES" >> $host-$port-global-vars.log