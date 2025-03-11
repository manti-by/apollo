# Apollo IoT module

[![Python3.11](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/downloads/release/python-3112/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/Apollo/master/LICENSE)

## About

Raspberry Pi monitoring app, a satellite for [Amon-Ra server](https://github.com/manti-by/amon-ra/)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/apollo/

Requirements:

- Raspberry Pi 2 Model B
- One DHT22 sensor
- Five DS1820 sensors
- Four ESP-01 with DHT11 satellites

## Setup Apollo application

1. Install [Python 3.11](https://www.python.org/downloads/release/python-3112/) and
create [a virtual environment](https://docs.python.org/3/library/venv.html) for the project.

2. Clone sources and install pip packages

    ```shell
    mkdir /home/manti/app/
    git clone https://github.com/manti-by/apollo app/
    pip install -r app/requirements.txt
    ```

3. Install crontabs

    ```cronexp
    */5 * * * *    cd /home/manti/app/ && /home/manti/app/venv/bin/python -m apollo.sensors
    ```

4. Run server

    ```shell
    cd /home/manti/app/
    uvicorn apollo.server:app --host 0.0.0.0 --reload
    ```
