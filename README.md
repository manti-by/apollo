Apollo IoT module
====

[![Python3.9](https://img.shields.io/badge/Python-3.9-green)](https://www.python.org/downloads/release/python-392/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/Apollo/master/LICENSE)

About
----

Raspberry Pi monitoring app, a satellite for [Helios Swarm](https://github.com/manti-by/helios/tree/swarm)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/apollo/tree/swarm

Requirements:

- Raspberry Pi 2 Model B
- DHT22 sensor

Setup Apollo Swarm application
----

1. Install python3.9, pip, virtualenv and sqlite3

    ```shell
    $ sudo apt install -y python3-pip virtualenv sqlite3
    ```
   
2. Create and activate virtualenv

    ```shell
    $ virtualenv -p python3 --prompt=apollo- /home/manti/venv
    $ source /home/manti/venv/bin/activate
    ```
   
3. Clone sources and install pip packages

    ```shell
    $ mkdir /home/manti/app/
    $ git clone -b swarm https://github.com/manti-by/apollo.git app/
    $ pip install -r app/requirements.txt
    ```

4. Install crontabs

    ```
    */5 * * * *    cd /home/pi/apollo/src/ && /home/pi/apollo/venv/bin/python -m apollo.sensors
    4-59/5 * * * * cd /home/pi/apollo/src/ && /home/pi/apollo/venv/bin/python -m apollo.proxy
    ```

5. Run server

    ```shell
    $ uvicorn apollo.server:app --host 0.0.0.0 --reload
    ```
   
Setup Helios application
----

Please check [README.md](https://github.com/manti-by/helios/tree/swarm) in Helios Swarm repository
for more details.
