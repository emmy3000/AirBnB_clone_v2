# File: 101-setup_web_static.pp

# Server configuration for web_static deployment.

$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://cuberule.com/;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '
<html>
  <head>
  </head>
  <body>
    Hello World courtesy of HBnB
  </body>
</html>
',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

exec { 'chown -R ubuntu:ubuntu /data/':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin/:/usr/local/bin/:/bin/',
}

file { '/var/www':
  ensure => 'directory',
}

file { '/var/www/html':
  ensure => 'directory',
}

file { '/var/www/html/index.html':
  ensure  => 'file',
  content => "Hello World courtesy of HBnB[web-02]\n",
}

file { '/var/www/html/404.html':
  ensure  => 'file',
  content => "Ceci n'est pas une page\n",
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_conf,
}

service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => Package['nginx'],
  subscribe => File['/etc/nginx/sites-available/default'],
}
