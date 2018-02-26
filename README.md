Apollo IoT App
==============


Server setup (Raspberry Pi 3 Model B)
-------------------------------------

NOTE: You can simply run setup_server.sh on your Raspberry PI

1. Install libraries on the server

        $ sudo apt-get install -y zip nginx supervisor postgresql
        $ sudo apt-get install -y python-pip python-dev python-virtualenv libpq-dev \
          libjpeg-dev libjpeg8-dev python-smbus


2. Clone sources, install app requirements and setup local config

        $ git clone git@github.com:manti-by/Apollo.git /home/pi/apollo/
        $ sudo pip install -r /home/pi/apollo/server/requirements.txt


3. Update server configs and start it

        $ sudo ln -s home/pi/apollo/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
        $ sudo service nginx restart

        $ sudo ln -s home/pi/apollo/src/deploy/confs/supervisor.conf /etc/supervisor/conf.d/apollo.conf
        $ sudo supervisorctl update
        $ sudo supervisorctl start apollo


4. Add worker crontab

        $ echo "*/5 * * * *    /usr/bin/python /home/pi/apollo/server/worker" | sudo tee -a /var/spool/cron/crontabs/pi
        $ echo "57 * * * *    /usr/bin/python /home/pi/apollo/server/scanner" | sudo tee -a /var/spool/cron/crontabs/pi



Sensor Setup (Arduino Nano V3.0 ATmega328P)
-------------------------------------------

1. Install Arduino system libraries 

        $ sudo apt-get install arduino arduino-core arduino-mk


2. Clone sources, compile firmware and upload to Arduino 

        $ git clone git@github.com:manti-by/Apollo.git
        $ cd Apollo/client/
        $ make
        $ make upload