import os
import sys
import datetime
import tarfile
import getpass
from random import randrange

def upgrade_system():
    os.system("yes|apt-get update")
    os.system("yes|apt-get upgrade")

def install_nginx():
    os.system("yes|apt-get install nginx")
    os.system("yes|ufw allow 'Nginx HTTP'")
    os.system("yes|ufw allow 'Nginx HTTPS'")
    os.system("yes|ufw allow 'Nginx Full'")
    os.system("yes|ufw allow 'OpenSSH'")
    os.system("yes|ufw enable")
    os.system("yes|ufw status")
    os.system("yes|systemctl status nginx")
    os.system("yes|systemctl start nginx")
    os.system("yes|systemctl enable nginx")
    os.system("yes|systemctl status nginx")

def setup_static_site(server):
    config_text='''server {
        listen 80;
        listen [::]:80;

        root /var/www/'''+server+'''/html;
        index index.html index.htm index.nginx-debian.html;

        server_name ''' +f'{server} www.{server}'+''';

        location / {
                try_files $uri $uri/ =404;
        }
    }
    '''
    comand_list = (
        f'mkdir -p /var/www/{server}/html',
        f'chown -R $USER:$USER /var/www/{server}/html',
        f'chmod -R 755 /var/www/{server}',
        f'mv {server} /etc/nginx/sites-available/{server}',
        f'ln -s /etc/nginx/sites-available/{server} /etc/nginx/sites-enabled/',
        f'nginx -t',
        f'systemctl restart nginx',
    )
    with open(server,'w') as f:
        f.write(config_text)
    for c in comand_list:
        os.system(c)

def install_certbot():
    os.system("yes|snap install core")
    os.system("yes|snap refresh core")
    os.system("yes|snap install --classic certbot")
    os.system("yes|ufw ln -s /snap/bin/certbot /usr/bin/certbot")

def get_ssl():
    os.system("certbot --nginx")


if __name__ == '__main__':
    try:
        os.system('clear')
        print('\n------------\nSERVER SETUP\n------------\n\n')
        print('0 - upgrade server')
        print('1 - install NGINX')
        print('2 - setup static site')
        print('3 - install CertBot')
        print('4 - get SSL certificate')
        print('other - exit')
        answer=input('Answer: ')

        if answer=='0':
            os.system('clear')
            print('\n------------\nUPGRADE SERVER\n------------\n\n')
            test=str(randrange(100))
            print('Input '+test)
            a=input('Answer: ')
            if a!=test:
                aaa=1/0
            upgrade_system()

        elif answer=='1':
            os.system('clear')
            print('\n------------\nINSTAL NGINX\n------------\n\n')
            test=str(randrange(100))
            print('Input '+test)
            a=input('Answer: ')
            if a!=test:
                aaa=1/0
            install_nginx()

        elif answer=='2':
            os.system('clear')
            print('\n------------\nSETUP STATIC SITE\n------------\n\n')
            url=input('URL(example.com): ')
            test=str(randrange(100))
            print(f'\nServer config for:\n{url}\nwww.{url}')
            print('Input '+test)
            a=input('Answer: ')
            if a!=test:
                aaa=1/0
            setup_static_site(url)

        elif answer=='3':
            os.system('clear')
            print('\n------------\nINSTAL CERTBOT\n------------\n\n')
            test=str(randrange(100))
            print('Input '+test)
            a=input('Answer: ')
            if a!=test:
                aaa=1/0
            install_certbot()
        
        elif answer=='4':
            os.system('clear')
            print('\n------------\nGET SSL\n------------\n\n')
            test=str(randrange(100))
            print('Input '+test)
            a=input('Answer: ')
            if a!=test:
                aaa=1/0
            get_ssl()

        print('\n----------\nDone! All OK!\n----------\n')
    except:
        print('\n----------\nSomething wrong!\n----------\n')