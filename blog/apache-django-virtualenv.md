---
layout: blog
title: Deploy Multiple Django Websites with Apache and Virtualenv
author: Tobias Hinz
blog_title: How to Serve Multiple Django Websites with Multiple Virtualenvs on Apache and mod_wsgi
date: 2019-04-10
description: how to set up your Ubuntu with Apache to serve multiple websites in parallel with the help of virtualenv and mod_wsgi
mathjax: true
comments: true
---
In this short guide we will describe how to set up an Apache server on Ubuntu 18.04 in order to serve multiple Django websites which use (potentially) different virtualenv environments[^1]. Specifically, this tutorial shows you how to:
1. Install Apache on your Ubuntu 18.04
2. Install mod_wsgi and virtualenv
3. Set Up Your Environment
4. Setting Up Your Django Website's wsgi.py file
5. Setting Up Apache to serve your Website Using a Specified virtualenv

In the end, you will have a system from which you can serve multiple websites in parallel, in the form

    www.myserver.com/website1
    www.myserver.com/website2
    ...

where, if necessary, all websites can use different virtualenvs. This is especially useful if your websites use different versions of Django or other packages which are not compatible between each other.

[^1]: This guide was written since it took us a while to get this specific configuration running, i.e. serving **multiple** Django websites on a current Ubuntu OS while using different virtualenvs for the different websites. Many of the tutorials we found were for older versions (e.g. Ubuntu 14) and did not serve **multiple** Django websites with **multiple** virtualenvs using only **one** Apache server.


# Prerequisites
We use the following OS and software versions, but later versions should (hopefully) also work:
* Ubuntu 18.04 LTS
* Python 3.6.6
* Apache 2.4.29
* virtualenv 16.0.0 (for Python 3)
* Django 2.1.2 (Python 3)
* mod_wsgi 4.6.4


# 1. Install Apache
We assume you have a running Ubuntu system on which you have sudo rights. The first step is to install the Apache server:

    sudo apt-get update
    sudo apt-get install apache2

During the installation, Apache registers itself with [UFW](https://help.ubuntu.com/lts/serverguide/firewall.html){:target="_blank"} to provide a few application profiles that can be used to enable or disable access to Apache through the firewall. List the ufw application profiles by typing:

    sudo ufw app list

The available applications should be:

    Apache: This profile opens only port 80 (normal, unencrypted web traffic) 
    Apache Full: This profile opens both port 80 (normal, unencrypted web traffic) and port 443 (TLS/SSL encrypted traffic) 
    Apache Secure: This profile opens only port 443 (TLS/SSL encrypted traffic) 
    OpenSSH: OpenSSH is a free implementation of the Secure Shell protocol.

Since we haven't configured SSL for our server yet, we will only need to allow traffic on port 80:

    sudo ufw allow 'Apache'

Now check that Apache is running:

    sudo systemctl status apache2

In your output you should have information about the status of the Apache server:

    Active: active (running) since Tue 2019-04-09 16:34:23 CEST; 18h ago

As a next step we'll install Apache-dev, which is needed for mod_wsgi:

    sudo apt-get install apache2-dev

In order to prevent any errors in your running system later check the settings in

    sudo nano /etc/apache2/envvars

For example, we had to add

    export LANG='en_US.UTF-8'
    export LC_ALL='en_US.UTF-8'

in order to have the correct encoding in our websites.
If you change anything with the language settings, make sure you have the necessary locales installed on the OS:

    locale -a

Now that we have the Apache server set up and running we will continue with the mod_wsgi package.


# 2. Install mod_wsgi and virtualenv
Remember that we use Python 3, so consider setting an alias in your `.bashrc` file to automatically use Python 3:

    alias python=python3

First, we'll install python-dev (check current version), distutils, and pip:

    sudo apt-get install python3.6-dev
    sudo apt install python3-distutils
    sudo apt-get install python3-pip

Now we are ready to install mod_wsgi for Python 3:

    sudo apt-get install libapache2-mod-wsgi-py3

Finally, install the virtualenv environment:

    pip3 install virtualenv


# 3. Set Up Your Environment
Now that we have installed the needed software packages we are ready to set up our environment for the usage of Django. First we create a folder from which we will later on host all our various websites:

    mkdir django_websites

Within this folder we also install our virtualenv, but you can also put your virtualenv(s) at any other location if you prefer:

    cd django_websites
    virtualenv django-virtualenv

Now activate the virtualenv and install the python packages you need for your first Django website that you want to host, e.g.

    source django-virtualenv/bin/activate
    pip install django
    pip install numpy
    ...

Now copy the folder containing your Django website into the current folder:

    cp -r django_website_1 django_websites

This folder should contain your database, your various apps, the `manage.py` file, and the folder containing the `settings.py` file. We will refer to the folder containing the `settings.py` file as `core` in this example:

    django_website_1
        middleware.py
        db.sqlite
        core
            settings.py
            ...
        app1
        app2
        ...


# 4. Setting Up The Website
As a first step we need to adapt the `wsgi.py` file in your Django app so that all the paths point to the location of your virtualenv. 

    nano /home/django_websites/django_website_1/core/wsgi.py

The final `wsgi.py` file should look something like this:

    import os
    import sys
    import site
    from django.core.wsgi import get_wsgi_application
    
    # Add the site-packages of the chosen virtualenv to work with
    site.addsitedir('/home/django_websites/django-virtualenv/lib/python3.6/site-packages')
    
    # Add the app's directory to the PYTHONPATH
    sys.path.append('/home/django_websites/django_website_1')
    sys.path.append('/home/django_websites/django_website_1/core')
    
    #to set enviroment settings for Django apps
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

    # Activate your virtual env
    activate_env=os.path.expanduser('/home/django_websites/django-virtualenv/bin/activate_this.py')
    exec(open(activate_env).read(), {'__file__': activate_env})
    
    application = get_wsgi_application()


# 5. Setting Up Apache to Serve the Website
In the next step we will adapt the Apache server's config file (e.g. `/etc/apache2/sites-available/000-default.conf`). 

    sudo nano /etc/apache2/sites-available/000-default.conf

Below the already existing configuration, but before the `</VirtualHost>` tag you can update the settings regarding your website. We add the following lines to point to the correct media and static folders (adapt to the location of your media and static folders, if you have any):

    Alias /media/ /home/django_websites/django_website_1/media/
    Alias /django_website_1/static/ /home/django_websites/django_website_1/static/

We also need to give Apache and mod_wsgi access to the required folders and files:

    <Directory /home/django_websites/django_website_1/static>
       Require all granted
    </Directory>
    
    <Directory /home/django_websites/django_website_1/media>
       Require all granted
    </Directory>
    
    <Directory /home/django_websites/django_website_1/core>
       <Files wsgi.py>
           Require all granted
       </Files>
    </Directory>

Finally, we need to make sure that Apache knows the link to the virtualenv. Below the previously added text we add the following lines, pointing it to the location of our virtualenv:

    WSGIDaemonProcess django_website_1 python-path=/home/django_websites/django_website_1:/home/django_websites/django-virtualenv/lib/python3.6/site-packages
    WSGIProcessGroup django_website_1
    WSGIScriptAlias /django_website_1 /home/django_websites/django_website_1/core/wsgi.py

The **first** line spawns a WSGI daemon process called `django_website_1` that is responsible for serving the Django application. The daemon name can essentially be anything but it is good practice to use descriptive names such as application names here. Since we are using a virtual environment we need to specify the alternate Python path so that mod_wsgi will know where to look for Python packages. The path must contain two directories, delimited by a colon: the directory of the Django project itself (`/home/django_websites/django_website_1`) and the directory of the Python packages inside our virtual environment for that project (`/home/django_websites/django-virtualenv/lib/python3.6/site-packages`). The **second** line tells that particular virtual host to use the WSGI daemon created beforehand and, as such, the daemon name must match between those two. The **third** line tells Apache and mod_wsgi where to find the WSGI configuration we modified in the previous step.


# 6. Setting Access Rights and Restarting Apache
Finally, assign the correct access rights (choose which access rights are the ones you need specifically) to your website(s) (specifically the database and the media/static folders) and restart the Apache server:

    sudo chmod -R 766 /home/django_websites/django_website_1/
    sudo service apache2 restart

You should now be able to access your website via

    www.myserver.com/django_website_1

If it is still now working check either the Apache error log for any errors

    cat /var/log/apache2/error.log

or try to run your website locally and see what kind of errors you get:

    /home/django_websites/django-virtualenv/bin/python /home/django_websites/django_website_1/manage.py runserver


# 7. Adding New Websites
If you want to add additional websites just add the folder containing the website files (and potentially a new virtualenv) to `/home/django_websites/` and continue with [4.](#4-setting-up-the-website), [5.](#5-setting-up-apache-to-serve-the-website), and [6.](#6-setting-access-rights-and-restarting-apache)
When modifying the Apache config file, add the new text blog underneath the already existing one for the previous website. **Do not mix/interleave these text blogs, but keep them separate in the config file**, e.g.

    Alias /media/ /home/django_websites/django_website_1/media/
    Alias /django_website_1/static/ /home/django_websites/django_website_1/static/
    <Directory /home/django_websites/django_website_1/static>
       Require all granted
    </Directory>
    <Directory /home/django_websites/django_website_1/media>
       Require all granted
    </Directory>
    <Directory /home/django_websites/django_website_1/core>
       <Files wsgi.py>
           Require all granted
       </Files>
    </Directory>
    WSGIDaemonProcess django_website_1 python-path=/home/django_websites/django_website_1:/home/django_websites/django-virtualenv/lib/python3.6/site-packages
    WSGIProcessGroup django_website_1
    WSGIScriptAlias /django_website_1 /home/django_websites/django_website_1/core/wsgi.py
    
    ###################
    
    Alias /media/ /home/django_websites/django_website_2/media/
    Alias /django_website_1/static/ /home/django_websites/django_website_2/static/
    <Directory /home/django_websites/django_website_2/static>
       Require all granted
    </Directory>
    <Directory /home/django_websites/django_website_2/media>
       Require all granted
    </Directory>
    <Directory /home/django_websites/django_website_2/core>
       <Files wsgi.py>
           Require all granted
       </Files>
    </Directory>
    WSGIDaemonProcess django_website_2 python-path=/home/django_websites/django_website_2:/home/django_websites/django-virtualenv-2/lib/python3.6/site-packages
    WSGIProcessGroup django_website_2
    WSGIScriptAlias /django_website_2 /home/django_websites/django_website_2/core/wsgi.py

If you want to delete any of the website, just delete the folder (and accompanying virtualenvs) from the `/home/django_websites/` folder and delete the corresponding text blog from the Apache config file.


# 8. Configure Default Apache Website
The default Apache website, i.e. the website that is shows when you access

    www.myserver.com

is located at 

    /var/www/html/index.html

You can update this file, e.g. by adding links to the various websites that you serve, in order to make it easier to access the different websites directly from the default webpage.

This concludes our guide to how to set up your system to serve multiple Django websites using different virtualenv with one Apache server. I hope this is useful for some of you. If you have any questions feel free to use the comments section below.

---
---

