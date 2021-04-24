#!/bin/python3
import os
import subprocess
import sys
import getpass

def update_system():
    os.system("yes|apt-get update")
    os.system("yes|apt-get upgrade")
    os.system("yes|apt-get install python3-pip")
    os.system("yes|apt-get install python3-venv")
    os.system("yes|apt-get install nginx")

def instal_django():

    now_command = 'sudo mkdir /var/site; sudo python3 -m venv /var/site/env'
    os.system(now_command)

    script_1 = '#!/bin/bash\nsource /var/site/env/bin/activate\npip3 install Django\ncd /var/site\ndjango-admin startproject ' + str(
        project_name) + '\npip3 install gunicorn'
    with open('script_1.sh', 'w') as f:
        f.write(script_1)
    now_command = 'chmod +x script_1.sh; ./script_1.sh; rm script_1.sh'
    os.system(now_command)

    start_gunicorn = '#!/bin/bash\nsource /var/site/env/bin/activate\nexec gunicorn -c "/var/site/' + str(
        project_name) + '/gunicorn_config.py" ' + str(project_name) + '.wsgi'
    with open('/var/site/' + str(project_name) + '/start_gunicorn.sh', 'w') as f:
        f.write(start_gunicorn)

    now_command = 'chmod +x /var/site/' + str(project_name) + '/start_gunicorn.sh'
    os.system(now_command)

    gunicorn_config = "command = '/var/site/env/bin/gunicorn'\n"
    gunicorn_config += "pythonpath='/var/site/" + str(project_name) + "/" + str(project_name) + "/'\n"
    gunicorn_config += "bind = '127.0.0.1:8001'\nworkers = 3\n"
    gunicorn_config += "user = '" + str(user_name) + "'\n"
    gunicorn_config += "limit_request_fields = 32000\nlimit_request_field_size = 0\nraw_env = 'DJANGO_SETTINGS_MODULE=" + str(project_name) + ".settings'"

    with open('/var/site/' + str(project_name) + '/gunicorn_config.py', 'w') as f:
        f.write(gunicorn_config)

    nginx_config = '''server {
            listen 80 default_server;
            listen [::]:80 default_server;

            root /var/www/html;

            index index.html index.htm index.nginx-debian.html;

            server_name _;

            location /static/ {
                    root /var/site/''' + str(project_name) + '''/;
            }

            location / {
                    proxy_pass http://127.0.0.1:8001;
                    proxy_set_header X-Forwarded-Host $server_name;
                    proxy_set_header X-Real-IP $remote_addr;
                    add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
                    add_header Access-Conrol-Allow-Origin *;
            }
    }'''
    with open('/etc/nginx/sites-enabled/default', 'w') as f:
        f.write(nginx_config)

    now_command = 'sudo service nginx restart'
    os.system(now_command)

    guni_service = '''[Unit]
    Descriptiom=Guni

    [Service]
    User=''' + str(user_name) + '''
    WorkingDirectory=/var/site/''' + str(project_name) + '''/
    VIRTUAL_ENV=/var/site/env
    Environment=PATH=$VIRTUAL_ENV/bin:$PATH

    ExecStart=/var/site/env/bin/gunicorn -c /var/site/''' + str(project_name) + '''/gunicorn_config.py ''' + str(project_name) + '''.wsgi
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target'''

    with open('/etc/systemd/system/guni.service', 'w') as f:
        f.write(guni_service)

    now_command = 'systemctl start guni.service; systemctl enable guni.service'
    os.system(now_command)


if __name__ == '__main__':

