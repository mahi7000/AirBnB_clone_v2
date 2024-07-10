#!/usr/bin/env bash
#Sets up your web servers for the deployment of webstatic

echo -e "Updating and doing some minor checks...\n"

function install() {
	command -v "$1" &> /dev/null

	#shellcheck disable=SC2181
	if [ $? -ne 0 ]; then
		echo -e "	Installing: $1$\n"
		sudo apt-get update -y -qq && \
			sudo apt-get install -y "$1" -qq
		echo -e "\n"
	else
		echo -e "	${1} is already installed.\n"
	fi
}

install nginx #install nginx

echo -e "\nSetting up some minor stuff.\n"

# allowing nginx on firewall
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

echo "<html>
  	<head>
  	</head>
  	<body>
    		Holberton School
  	</body>
      </html>" > /data/web_static/releases/test/index.html


if [ -L /data/web_static/current ]; then
	rm /data/web_static/current
fi

suodo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo bash -c 'cat > /etc/nginx/sites-available/web_static' <<EOF
server {
    listen 80;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}
EOF

sudo service nginx restart
