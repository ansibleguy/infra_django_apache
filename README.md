<a href="https://www.djangoproject.com">
<img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" alt="Django Logo" width="300"/>
</a>

# Ansible Role - Python3 Django

Ansible Role to deploy one or multiple Django applications on a linux server using Apache2 as webserver.

<a href='https://ko-fi.com/ansible0guy' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy me a coffee' />

[![Molecule Test Status](https://badges.ansibleguy.net/infra_django_apache.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_django_apache.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_django_apache.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_django_apache.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/ansibleguy/infra_django_apache)

Molecule Logs: [Short](https://badges.ansibleguy.net/log/molecule_infra_django_apache_test_short.log), [Full](https://badges.ansibleguy.net/log/molecule_infra_django_apache_test.log)

**Tested:**
* Debian 11

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/ansibleguy/infra_django_apache

# from galaxy
ansible-galaxy install ansibleguy.infra_django_apache

# or to custom role-path
ansible-galaxy install ansibleguy.infra_django_apache --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

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


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main/site defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


## Usage

You want a simple Ansible GUI? Check-out my [Ansible WebUI](https://github.com/ansibleguy/webui)

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
