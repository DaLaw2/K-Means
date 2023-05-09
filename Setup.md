# K-Means Web Setup
###### Tags: `Other` `K-Means`
## Update apt
To make sure we have the latest packages, update apt with the following command:
```
apt update
```
## Install PHP
Install the necessary PHP packages:
```
apt install php-fpm php-mbstring php-pear php-dev -y
```
Check the PHP version:
```
php -v
```
This will output something similar to:
```
PHP 8.1.2-1ubuntu2.11 (cli) (built: Feb 22 2023 22:56:18) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.1.2, Copyright (c) Zend Technologies
    with Zend OPcache v8.1.2-1ubuntu2.11, Copyright (c), by Zend Technologies
```
Now we know that the installed PHP version is **8.1**.

Start the PHP service by replacing **php8.1** with your PHP version:
```
service php8.1-fpm start
```
## Install Nginx
Install Nginx and vim for editing files:
```
apt install nginx vim -y
```
Edit the default Nginx configuration file:
```
vim /etc/nginx/sites-available/default
```
The original file looks like this: **(Ignore useless annotation)**
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }
        
        #location ~ \.php$ {
        #       include snippets/fastcgi-php.conf;
        #
        #       # With php-fpm (or other unix sockets):
        #       fastcgi_pass unix:/run/php/php7.4-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        #}

}
```
Add **index.php** to the index line and add **server name** with **127.0.0.1**.

Uncomment the PHP configuration lines and replace **php8.1** with your PHP version in the fastcgi_pass line, as follows:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.php index.html index.htm index.nginx-debian.html;

        server_name 127.0.0.1;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }
        
        location ~ \.php$ {
               include snippets/fastcgi-php.conf;
        #
        #       # With php-fpm (or other unix sockets):
               fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }

}
```
Test the Nginx configuration file:
```
nginx -t
```
If successful, you will see:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
Start Nginx:
```
service nginx start
```
Nginx uses the user:**www-data** to run the service, so we need to grant permission to the user:
```
usermod -aG sudo www-data
```
## Install Composer
Download the Composer source from the internet:
```
curl -sS https://getcomposer.org/installer | php
```
Add Composer to the system path:
```
mv composer.phar /usr/local/bin/composer
```
Modify the execution permission of the Composer command:
```
chmod +x /usr/local/bin/composer
```
Execute the command to view the help and verify the installation:
```
composer
```
## Install MongoDB Extension
Navigate to your web root (default is **"/var/www/html/"**):
```
cd /var/www/html
```
Install the MongoDB extension:
```
pecl install mongodb
```
Configure the MongoDB extension:
```
echo "extension=mongodb.so" >> `php --ini | grep "Loaded Configuration" | sed -e "s|.*:\s*||"`
```
Open the PHP configuration file:
```
vim /etc/php/8.1/fpm/php.ini
```
Add the following line at the end of the file:
```
extension=mongodb.so
```
Install Git:
```
apt install git -y
```
Allow your web application to use the MongoDB extension:
```
composer require mongodb/mongodb
```
