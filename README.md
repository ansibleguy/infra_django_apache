# MariaDB Multi-Instance Ansible Role
Ansible role to install one or multiple MariaDB instances on the target server.

**Tested:**
* Debian 11

## Functionality

* Package installation
  * Ansible dependencies (_minimal_)
  * 
* Configuration
  * 
  * Default opt-in:
    * 
  * Default opt-outs:
    * 
  * Default config:
    * 
## Infos

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


## Usage
Run the playbook/role:
```bash
ansible-playbook -K -D -i inventory/hosts.yml mariadb.yml --ask-vault-pass
```

You need to define your instances by configuring the 'mariadb' dictionary!

```yaml
mariadb:
  service:
    SyslogIdentifier: 'mariadb_ag_%I'  # %I = Instance-Key
    
  instances:
    api:
      root_pwd: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        64373031333937633163366236663237623464336461613334343739323763373330393930666331
        3333663262346337636536383539303834373733326631310a393865653831663238383937626238
        35396531316338373030353530663465343838373635363633613035356338353366373231343264
        3437356663383466630a666161363163346533333139656566386466383733646134616166376638
        35313765356134396130333439663461353336313230366338646165376666313232

      dbs:
        api:
        templates:
        deprecated: 'absent'
      
      users:
        app:
          priv: 'api.*:ALL'
          pwd: !vault ...
        guy:
          priv: 'api.*:SELECT,SHOW VIEW'
          state: 'absent'
          pwd: !vault ...

      settings:
        # port: 3306
        innodb_log_file_size: 5G
        max_connections: 2000

      backup:
        enabled: true
        dbs: ['api']
        time: '*-*-* 01:00'  # for syntax see: https://wiki.archlinux.org/title/Systemd/Timers
        creds:
          create: true

    test:
      ansible_user: 'not_root'
      ansible_pwd: !vault ...
      dbs:
        test:
          
      users:
        dummy:
          priv: 'test.*:ALL'
          pwd: !vault ...
          update_pwd: 'always'  # else it will only be set on creation; changing the password always might bring problems with active-active replications

      settings:
        port: 3307
        log_warnings: 4
        long_query_time: 2
        max_allowed_packet: 2G

    old_instance:
      state: 'absent'

```

There are also some useful **tags** available:
* base => only configure basics; instances will not be touched
* instances
* config => configuration (base and instances)
* dbs
* backup => instance backup-jobs
* users


You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Example


**Config**
```yaml
mariadb:
  instances:
    guydb:
      root_pwd: !vault ...

      dbs:
        nice:
        memes:

      users:
        django:
          priv: 'backup.creds.defaults_file is not nonmemes.*:ALL'
          pwd: !vault ...
        backup:
          priv: '*.*:SELECT,RELOAD,PROCESS,LOCK TABLES,BINLOG MONITOR,SHOW VIEW,EVENT,TRIGGER'
          pwd: !vault ...

```

**Result:**
```bash
# config directories
guy@ansible:~# tree /etc/mysql
> /etc/mysql/
> ├── conf.d
> │   ├── mysql.cnf
> │   └── mysqldump.cnf
> ├── debian.cnf
> ├── debian-start  # default instance start-script
> ├── debian-start-instance.sh  # multi-instance start-script
> ├── instance.conf.d  # instance configurations
> │   ├── client_guydb_startup-checks.cnf  # login data for startup-check service-user
> │   └── server_guydb.cnf  # instance server config
> ├── mariadb.cnf  # default instance config
> ├── mariadb.conf.d
> ├── my.cnf -> /etc/alternatives/my.cnf
> └── my.cnf.fallback

# data directories
guy@ansible:~# tree /var/lib/mysql
> /var/lib/mysql/
> ├── default
> │  └── ...  # mysql default instance
> │
> ├── instance_guydb
> │  └── ...  # configured instance
> │
> └── ...  # default files => not automatically cleaned

# instance config-file
guy@ansible:~# cat /etc/mysql/instance.conf.d/server_guydb.cnf 
> # Ansible managed
> [mysqld]
> datadir = /var/lib/mysql/instance_guydb
> basedir = /usr
> pid-file = /run/mysqld/mysqld_guydb.pid
> socket = /run/mysqld/mysqld_guydb.sock
> lc_messages_dir = /usr/share/mysql
> 
> # settings
> user = mysql
> group = mysql
> bind_address = 127.0.0.1
> port = 3306
> log_warnings = 2
> character-set-server = utf8mb4
> collation-server = utf8mb4_general_ci
> innodb_file_per_table = 1
> innodb_buffer_pool_size = 512M
> innodb_log_file_size = 1GB
> max_allowed_packet = 512M
> max_connections = 500
> skip-name-resolve
> query_cache_size = 64M
> tmp_table_size = 64M
> max_heap_table_size = 64M
> slow-query-log = 1
> slow-query-log-file = slow-queries.log
> long_query_time = 1
> wait_timeout = 60
> symbolic-links = 0
> local-infile = 0
> open_files_limit = 1048576

# service config
guy@ansible:~# cat /etc/systemd/system/mariadb@.service.d/override.conf 
> # Ansible managed
> 
> [Unit]
> ConditionPathExists=/etc/mysql/instance.conf.d/server_%I.cnf
> ConditionPathExists=/etc/mysql/debian-start-instance.sh
> ConditionPathExists=/etc/mysql/instance.conf.d/client_%I_startup-checks.cnf
> Documentation=https://github.com/ansibleguy/infra_mariadb
> 
> [Service]
> Environment='MYSQLD_MULTI_INSTANCE=--defaults-file=/etc/mysql/instance.conf.d/server_%I.cnf --defaults-group-suffix=.%I'
> ExecStartPost=
> ExecStartPost=/etc/mysql/debian-start-instance.sh %I
> 
> LimitNOFILE=1048576
> StandardOutput=journal
> StandardError=journal
> SyslogIdentifier=mariadb_%I
> TimeoutStartSec=900
> TimeoutStopSec=900
> Restart=on-abort
> RestartSec=5s
> OOMScoreAdjust=-600
> BlockIOWeight=1000

# service status
guy@ansible:~# systemctl status mariadb@guydb.service 
> ● mariadb@guydb.service - MariaDB 10.5.12 database server (multi-instance guydb)
>      Loaded: loaded (/lib/systemd/system/mariadb@.service; enabled; vendor preset: enabled)
>     Drop-In: /etc/systemd/system/mariadb@.service.d
>              └─override.conf
>      Active: active (running)
>        Docs: man:mariadbd(8)
>              https://mariadb.com/kb/en/library/systemd/
>              https://github.com/ansibleguy/infra_mariadb
>     Process: 134872 ExecStartPre=/usr/bin/mysql_install_db $MYSQLD_MULTI_INSTANCE (code=exited, status=0/SUCCESS)
>     Process: 134910 ExecStartPost=/etc/mysql/debian-start-instance.sh guydb (code=exited, status=0/SUCCESS)
>      Status: "Taking your SQL requests now..."
>      CGroup: /system.slice/system-mariadb.slice/mariadb@guydb.service
>              └─134898 /usr/sbin/mariadbd --defaults-file=/etc/mysql/instance.conf.d/server_guydb.cnf --defaults-group-suffix=.guydb

# databases
guy@ansible:~# mysql --socket=/run/mysql/mysqld_guydb.sock -p -e "show databases;"
> +--------------------+
> | Database           |
> +--------------------+
> | nice               |
> | memes              |
> | information_schema |
> | mysql              |
> | performance_schema |
> +--------------------+

# mysql users
guy@ansible:~# mysql --socket=/run/mysql/mysqld_guydb.sock -p -e "select user, host from mysql.user;"
> +------------------------+-----------+
> | User                   | Host      |
> +------------------------+-----------+
> | backup                 | localhost |
> | django                 | localhost |
> | mariadb.sys            | localhost |
> | mariadb_startup_checks | localhost |  # needed service-user for startup-script (upgrade tasks and so on)
> | mysql                  | localhost |
> | root                   | localhost |
> +------------------------+-----------+

# mysql privileges
guy@ansible:~# mysql --socket=/run/mysql/mysqld_guydb.sock -p -e "show grants for django@localhost;"
> +---------------------------------------------------------------------------+
> | Grants for django@localhost                                               |
> +---------------------------------------------------------------------------+
> | GRANT USAGE ON *.* TO `django`@`localhost` IDENTIFIED BY PASSWORD 'XXXX'  |
> | GRANT ALL PRIVILEGES ON `memes`.* TO `django`@`localhost`                 |
> +---------------------------------------------------------------------------+

guy@ansible:~# mysql --socket=/run/mysql/mysqld_guydb.sock -p -e "show grants for backup@localhost;"
> +------------------------------------------------------------------------------------------------+
> | Grants for backup@localhost                                                                    |
> +------------------------------------------------------------------------------------------------+
> | GRANT SELECT, RELOAD, PROCESS, LOCK TABLES, BINLOG MONITOR, SHOW VIEW, EVENT, TRIGGER ON *.*   |
> | TO `backup`@`localhost` IDENTIFIED BY PASSWORD 'XXXX'                                          |
> +------------------------------------------------------------------------------------------------+


```