# Tap 2 Eat Web Implementation

Please check the github issues page before implementation.

#### Project layout

Path | Description
-----|------------
home/ | Project root (created by django-admin startproject). Home to README.md and Django's manage.py script.
invoicemanager/attachments/ | FS location for attachment storage (located **OUTSIDE** the application root)
invoicemanager/db.sqlite3 | SQLite3 database file (located **OUTSIDE** the application root). Created when running 'python manage.py migrate'. Will not be present if you go straight to MySQL.
invoicemanager/invoicemanager/ | Application root
invoicemanager/invoicemanager/static/ | Static files (CSS, JS, etc)
invoicemanager/invoicemanager/wsgi.py | Python WSGI script for Apache integration


### Basic Installation
* This guide assumes Debian/Ubuntu is the running OS. Administrative rights are obtained using **sudo**.
* RPM-based systems should be similar. Windows is theoretically possible but untested.
* The application will be installed to **/opt/invoicemanager**
* Basic installation will get the application up and running, however it is not suitable for production use

1. Clone the repo then Install pip
```bash
$ sudo apt-get install python3 python3-pip
```

2. Update pip3 to latest version (using sudo with pip requires the -H flag)
```bash
$ sudo -H pip3 install --upgrade pip
```

3. Install Requirements.txt file
```bash
$ pip3 install -r requirements.txt
```

5. Edit the following lines of mainapp/settings.py to match your environment
```python
#  Put a random string at least 50 characters long here. This will keep hashed passwords safe.
SECRET_KEY = 'abcdefgsflxushdfmilsdhfidjsnhcfgiksjfgikdhgisldgiemlgnilehw59y349yjwe9'
```

6. Create the application database
```bash
/mainapp$ sudo python3 manage.py migrate
```

7. Create an admin user
```bash
/mainapp$ sudo python3 manage.py create superuser
Username (leave blank to use 'root'): admin
Email address: admin@home.local
Password:
Password (again):
Superuser created successfully.
```

8. At this point, you should have enough configured to run the app using Python's development server. Run the following command and browse to http://hostIp:8000
```bash
/mainapp$ $ sudo python3 manage.py migrate $$ sudo python3 manage.py runserver 0.0.0.0:8000
```
9. Edit the following lines of mainapp/settings.py to add domain name/IP
```python
#add domain or host
ALLOWED_HOSTS = ['tap2eat.co.ke', '35.234.432.12']
```

### Using MySQL instead of SQLite3
1. Install MySQL client and Python MySQL driver
```bash
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
$ pip3 install mysqlclient
```

2. Create the MySQL database and user
```bash
$ mysql -u root -p [-h servername]
```
```sql
create database 'databasename';
exit;
```

4. Update mainapp/settings.py. Find the 'DATABASES' section, comment the sqlite database settings and uncomment the mysql settings.
```python
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Use settings below for local sqlite file

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#                 'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# Use settings below for MySQL server (requires python-mysql)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'databasename',
        'USER': 'databasename',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'servername',
        'PORT': '',
    }
}
```

### Using a production web server
It is highly recommended to use a 'real' web server for running. This example uses apache, however any wsgi-compatible server will work.

1. Install apache and wsgi module
```bash
$ sudo apt-get install apache2 libapache2-mod-wsgi-py3
$ sudo a2enmod wsgi
```

2. Edit apache config to use wsgi.py included with static and attachments directories
```bash
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

```apacheconf
# These lines must be outside of the VirtualHost directive
WSGIScriptAlias / mainapp/mainapp/wsgi.py
WSGIPythonPath /mainapp/mainapp

<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /mainapp>
                Options Indexes MultiViews FollowSymLinks
                Require all granted
        </Directory>

        <Directory /mainapp/mainapp>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

		# The real location of these directories can be moved if desired.
        # Remember to update mainapp/settings.py to reflect changes here.
        Alias /static mainapp/tap2eat/static
</VirtualHost>
```

3. Restart apache and headover to your IP.
```bash
$ sudo service apache2 restart
```
