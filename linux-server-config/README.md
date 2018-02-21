# Linux Server Configuration

This is the third project of the Full Stack Nano Degree II by Udacity.

Access the live WebApp [Science Digest](http://35.185.137.139)

---

#### IP-Address: 35.185.137.139
#### URL: [http://35.185.137.139](http://35.185.137.139)

---

## Summamry of software installed

* Apache2 - ```sudo apt-get install apache2```
* pip - ```sudo apt-get install python-pip```
* Postgresql - ```sudo apt-get install postgresql postgresql-contrib```
* SQLAlchemy - ```sudo pip install sqlalchemy```
* Flask - ```sudo pip install flask```
* Dependencies - ```sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlalchemy_utils```

---
## Summary of configurations made

* Setting timezone to UTC:
```sudo timedatectl set-timezone UTC```
* Configuring Postgresql:
```
Creating user catalog with database catalog.
```
* Configuring wsgi:
```
<VirtualHost *:80>
	ServerName 35.185.137.139
	ServerAdmin thakursaurabh1998@gmail.com
	WSGIDaemonProcess views python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
	WSGIProcessGroup views
	WSGIScriptAlias / /var/www/catalog/views.wsgi
	WSGIDaemonProcess views user=local-user group=local-user threads=25
	<Directory /var/www/catalog/>
		Order allow,deny
		Allow from all
	</Directory>
	Alias /static /var/www/catalog/static
	<Directory /var/www/catalog/static/>
		Order allow,deny
		Allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
 ```
 * Configuring .wsgi file:
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from views import app as application
```

---
Help Taken From: [Flask Documentation](https://flask.pocoo.org), [AskUbuntu](https://askubuntu.com)

Server up and running on [Google Cloud Compute Engine](https://cloud.google.com/compute)