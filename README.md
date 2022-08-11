[![Django](https://static.djangoproject.com/img/logos/django-logo-negative.svg)](https://www.djangoproject.com)

# Ansible Role - Python3 Django
Ansible Role to deploy one or multiple Django applications on a linux server using Apache2 as webserver.

[![Ansible Galaxy](https://img.shields.io/ansible/role/56812)](https://galaxy.ansible.com/ansibleguy/infra_django_apache)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F56812%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_django_apache)

**Tested:**
* Debian 11

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * Apache using [THIS](https://github.com/ansibleguy/infra_apache) role
  * Support for MySQL or PostgreSQL

  * **Default opt-in**:
    * MariaDB database using [THIS](https://github.com/ansibleguy/infra_mariadb) role


  * **Default opt-outs**:
    * Database backup service
    * Special apache config => can be passed using the 'django' dictionary
    * Running 'collectstatic'


  * **Default config**:
    * A Self-Signed certificate will be used
    * Database type => MariaDB
      * Database will be installed automatically 
    * Using a python virtual environment
    * A database migration script will be created in the venv directory

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


## Usage

### Config

You need to define your instances by configuring the 'mariadb' dictionary!

```yaml
django:
  sites:
    niceApp:
      domain: 'django.ansibleguy.net'
      project: 'super'  # the directory containing the 'settings.py' is named like this 
      
      sync_code:  # sync's local code to the remote server
        enabled: true
        src: '/home/ansibleguy/code/niceApp'
        static_src: '/home/ansibleguy/code/niceApp_static'
      
      venv: '/var/lib/niceApp'

      python_modules:
        present: ['netaddr', 'pycryptodome']
      
      env_pythonpath: ['/var/lib/myOtherApp']  # will get added to django's PYTHONPATH environmental variable

      ssl:
        mode: 'letsencrypt'

      letsencrypt:
        email: 'django@template.ansibleguy.net'
```

You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook/role:
```bash
ansible-playbook -K -D -i inventory/hosts.yml django.yml --ask-vault-pass
```

There are also some useful **tags** available:
* base => only configure basics; instances will not be touched
* sites
* config
* db
* sync => only sync local code to remote host (_if enabled by user_)
* django => don't start sub-roles for apache and/or mariadb

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
