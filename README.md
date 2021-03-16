 # ~~mysql57_vs_8-benchmark_scripts~~

~~Benchmarking scripts for MySQL 5.7  vs MySQL 8.0 ~~

Benchmarking scripts for MySQL 8.0(Local FS) vs MySQL 8.0(Fast CFS) 

## Install Two MySQL

```shell
groupadd mysql
useradd -r -g mysql -s /bin/false mysql
cd /usr/local
tar xvf /path/to/mysql-VERSION-OS.tar.xz
ln -s full-path-to-mysql-VERSION-OS mysql
cd mysql
mkdir mysql-files
chown mysql:mysql mysql-files
chmod 750 mysql-files
bin/mysql_ssl_rsa_setup

```

/etc/my.cnf
```
[mysqld]
datadir=/usr/local/mysql/data
socket=/tmp/mysql.sock
port=3306
log-error=/usr/local/mysql/data/localhost.localdomain.err
user=mysql
secure_file_priv=/usr/local/mysql/mysql-files
local_infile=OFF

[mysqld@cfs]
datadir=/usr/local/fastcfs/fuse/fuse1/mysql/data
socket=/tmp/mysql_cfs.sock
port=3307
log-error=/usr/local/mysql/data/localhost.cfs.err
user=mysql
secure_file_priv=/usr/local/mysql/mysql-files
local_infile=OFF
```

### Local MySQL
```shell
cd /usr/local/mysql
mkdir data
chmod 750 data
chown mysql:mysql data

mysqld --defaults-file=/etc/my.cnf --initialize
```

### FastCFS MySQL
```
cd /usr/local/fastcfs/fuse/fuse1/
mkdir mysql && cd mysql && mkdir data
chmod 750 data
chown mysql:mysql data
# init
mysqld --user=mysql --initialize \
  --datadir=/usr/local/fastcfs/fuse/fuse1/mysql/data \
  --socket=/tmp/mysql_cfs.sock \
  --port=3307 \
  --log-error=/usr/local/mysql/data/localhost.cfs.err \
  --secure_file_priv=/usr/local/mysql/mysql-files \
  --local_infile=OFF
```

### Systemctl

create mysqld.service for Mysql of Local FS


```
shell> cd /usr/lib/systemd/system
shell> touch mysqld.service
shell> chmod 644 mysqld.service
```

```
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql

# Have mysqld write its state to the systemd notify socket
Type=notify

# Disable service start and stop timeout logic of systemd for mysqld service.
TimeoutSec=0

# Start main service
ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf $MYSQLD_OPTS 

# Use this to switch malloc implementation
EnvironmentFile=-/etc/sysconfig/mysql

# Sets open_files_limit
LimitNOFILE = 10000

Restart=on-failure

RestartPreventExitStatus=1

# Set environment variable MYSQLD_PARENT_PID. This is required for restart.
Environment=MYSQLD_PARENT_PID=1

PrivateTmp=false
```

for FastCFS
```
cp mysqld.service mysqld_cfs.service

# ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf --defaults-group-suffix=@%I $MYSQLD_OPTS
```

### StartUp
```
systemctl start mysqld
systemctl start mysqld@cfs
```

change password
```
mysql -uroot -p
mysql -uroot -S/tmp/mysql_cfs.sock -p


ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';

```

## Grant Privileges

```
use mysql;
CREATE USER 'root'@'192.168.99.1' IDENTIFIED BY 'chwing';
GRANT ALL ON *.* TO 'root'@'192.168.99.1';
flush privileges;
```

## bench

Reference https://severalnines.com/database-blog/mysql-performance-benchmarking-mysql-57-vs-mysql-80

### prebench

* intstall[stsbench](https://github.com/akopytov/sysbench)

```
mysql> create database sbtest;
```

## to bench
```
./sb/prepare.sh
./sb/run.sh
```

## csv to graph
```
python3 to_graph.py 192.168.99.113-3306-local 192.168.99.113-3307-cfs
```
