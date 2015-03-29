- Install moin via pip:

  pip install moin

- Configure crontab to run moin on reboot, e.g.:

  @reboot /home/ubuntu/misc/moin/runmoin.sh

- Add the following snippet to the apache config:

LoadModule proxy_module /usr/lib/apache2/modules/mod_proxy.so
LoadModule proxy_http_module /usr/lib/apache2/modules/mod_proxy_http.so

<VirtualHost *:80>
    ServerName wiki.juanl.org

    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/
    <Location />
        Order allow,deny
        Allow from all
    </Location>
</VirtualHost>

# Adding a new user to MoinMoin

    moin --config-dir=/usr/local/share/moin/ \
         --wiki-url=http://wiki.juanl.org \
         account create \
         --name="username" \
         --password="password" \
         --email="email" \
         --alias="username"
