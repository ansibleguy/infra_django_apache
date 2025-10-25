<a href="https://www.djangoproject.com">
<img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" alt="Django Logo" width="300"/>
</a>

# Ansible Role - Python3 Django

Ansible Role to deploy one or multiple Django applications on a linux server using Apache2 as webserver.

[![Lint](https://github.com/O-X-L/ansible-role-django-apache2/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/ansible-role-django-apache2/actions/workflows/lint.yml)
[![Ansible Galaxy](https://badges.oss.oxl.app/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/oxlorg/django_apache2)

**Molecule Integration-Tests**:

* Status: [![Molecule Test Status](https://badges.oss.oxl.app/infra_django_apache.molecule.svg)](https://github.com/O-X-L/ansible-role-oxl-cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2) |
[![Functional-Tests](https://github.com/O-X-L/ansible-role-django-apache2/actions/workflows/integration_test_result.yml/badge.svg)](https://github.com/O-X-L/ansible-role-django-apache2/actions/workflows/integration_test_result.yml)
* Logs: [API](https://ci.oss.oxl.app/api/job/ansible-test-molecule-infra_django_apache/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) | [Short](https://badges.oss.oxl.app/log/molecule_infra_django_apache_test_short.log) | [Full](https://badges.oss.oxl.app/log/molecule_infra_django_apache_test.log)

Internal CI: [Tester Role](https://github.com/O-X-L/ansible-role-oxl-cicd) | [Jobs API](https://github.com/O-X-L/github-self-hosted-jobs-systemd)

**Tested:**
* Debian 11
* Debian 12

----

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/O-X-L/ansible-role-django-apache2

# from galaxy
ansible-galaxy install oxlorg.django_apache2

# or to custom role-path
ansible-galaxy install oxlorg.django_apache2 --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

----

## Advertisement

* Need **professional support** using Ansible or managing Web-Applications? Contact us:

  E-Mail: [contact@oxl.at](mailto:contact@oxl.at)

  Tel: [+43 3115 40 900 0](tel:+433115409000)

  Web: [EN](https://www.o-x-l.com) | [DE](https://www.oxl.at)

  Language: German or English

* You want a simple **Ansible GUI**?

  Check-out this [Ansible WebUI](https://github.com/O-X-L/ansible-webui)

----

## Usage

### Config

You need to define your instances by configuring the 'mariadb' dictionary!

```yaml
django:
  sites:
    niceApp:
      domain: 'django.oxl.at'
      project: 'super'  # the directory containing the 'settings.py' is named like this 
      
      sync_code:  # sync's local code to the remote server
        enabled: true
        src: '/home/oxlorg/code/niceApp'
        static_src: '/home/oxlorg/code/niceApp_static'
      
      venv: '/var/lib/niceApp'

      python_modules:
        present: ['netaddr', 'pycryptodome']
      
      env_pythonpath: ['/var/lib/myOtherApp']  # will get added to django's PYTHONPATH environmental variable

      ssl:
        mode: 'letsencrypt'

      letsencrypt:
        email: 'django@template.oxl.at'
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

----

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * Apache using [THIS](https://github.com/O-X-L/ansible-role-apache2) role
  * Support for MySQL or PostgreSQL

  * **Default opt-in**:
    * MariaDB database using [THIS](https://github.com/O-X-L/ansible-role-mariadb) role


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

----

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main/site defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!

