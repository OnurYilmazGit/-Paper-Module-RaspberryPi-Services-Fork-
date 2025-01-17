e-Paper Module Raspberry Pi Services

e-Paper Module Raspberry Pi Services
====================================

This project is a fork of the e-Paper Module Raspberry Pi Services. It provides a set of microservices for controlling an e-Paper module using a Raspberry Pi.

Table of Contents
-----------------

*   [Installation](#installation)
*   [Running the Main Script](#running-the-main-script)
*   [Microservices](#microservices)


Installation
------------

### Working With Raspberry Pi

**Hardware Connection:** When connecting the Raspberry Pi, you can directly insert the board into the 40PIN pin header of the Raspberry Pi, paying attention to the correct pins. If you choose to connect with an 8PIN cable, please refer to the pin correspondence table below:

| e-Paper | Raspberry Pi |
|---------|--------------|
| VCC     | 3.3V         |
| GND     | GND          |
| DIN     | 19           |
| CLK     | 23           |
| CS      | 24           |
| DC      | 22           |
| RST     | 11           |
| BUSY    | 18           |



### Enable SPI Interface

1.  Open the Raspberry Pi terminal and enter the following command in the config interface:

    sudo raspi-config

3.  Choose Interfacing Options -> SPI -> Yes to enable the SPI interface.
4.  Reboot your Raspberry Pi:

    sudo reboot

6.  Check `/boot/config.txt` to ensure that 'dtparam=spi=on' is written.

### Install Dependencies

#### Install BCM2835

1.  Open the Raspberry Pi terminal and run the following commands:

    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz

    tar zxvf bcm2835-1.71.tar.gz

    cd bcm2835-1.71/

    sudo ./configure && sudo make && sudo make check && sudo make install

For more information, please refer to the official website: [http://www.airspayce.com/mikem/bcm2835/](http://www.airspayce.com/mikem/bcm2835/)

#### Install WiringPi (Optional)

1.  Open the Raspberry Pi terminal and run the following commands:

    sudo apt-get install wiringpi

For Raspberry Pi systems after May 2019, you may need to upgrade:

    wget https://project-downloads.drogon.net/wiringpi-latest.deb

    sudo dpkg -i wiringpi-latest.deb

    gpio -v

Run `gpio -v` and make sure version 2.52 appears. If it does not appear, the installation is incorrect.

### Download and Compile the Demo

1.  Download the demo via GitHub:

    git clone https://github.com/waveshare/e-Paper.git

    cd e-Paper/RaspberryPi_JetsonNano/

4.  Compile the demo:

    sudo apt-get install p7zip-full

    wget  https://www.waveshare.com/w/upload/3/39/E-Paper_code.7z

    7z x E-Paper_code.7z -O./e-Paper

    cd e-Paper/RaspberryPi_JetsonNano/

    cd c

    sudo make clean

    sudo make -j4 EPD=epd1in54V2

### Install Python Dependencies

#### Python 3

1.  Open the Raspberry Pi terminal and run the following commands:

    sudo apt-get update

    sudo apt-get install python3-pip

    sudo apt-get install python3-pil

    sudo apt-get install python3-numpy

    sudo pip3 install RPi.GPIO

    sudo pip3 install spidev

#### Python 2 (Optional)

1.  Open the Raspberry Pi terminal and run the following commands:

    sudo apt-get update

    sudo apt-get install python-pip

    sudo apt-get install python-pil

    sudo apt-get install python-numpy

    sudo pip install RPi.GPIO

    sudo pip install spidev

### Running the Main Script

Before using the microservices, you need to run the main script, which starts the Flask server. Follow these steps:

1.  Open a terminal and navigate to the project directory.
    cd e-Paper/RaspberryPi_JetsonNano/python/examples
3.  Run the main script:
    python3 main.py

The Flask server will start running on port 9920.

### Basic Usage of Microservices

Once the main script is running, you can use the microservices via separate terminal sessions or by sending requests from a browser or other client. Refer to the microservice descriptions for the specific commands to use.
The following microservices are available:

*   **Clear Screen:**

    curl -X PUT http://localhost:9920/clearScreen

*   **Display Image:**

    curl -X POST -F "image=@/path_to_your_image.jpg" http://localhost:9920/displayImage

*   **Display Cross:**

    curl -X PUT http://localhost:9920/displayCross

*   **Display Text:**

    curl -X POST -F "text=Hello World" http://localhost:9920/displayText


Please refer to the original documentation for further details and advanced usage.

**Note:** Make sure to provide proper permissions and access rights while executing the commands.


# Daemonizing a Flask Application with Systemd

This guide outlines the steps to daemonize your Flask application using `systemd` on Linux systems.

## Prerequisites

- Linux system with `systemd` installed.
- Python and Flask installed.

## Steps

1. **Create a Systemd Service File:**

   - Create a new service file with a unique name and the `.service` extension. For example, let's use the name "e-paper-display-app.service".
   - Open the file and enter the following content:

     ```plaintext
     [Unit]
     Description=E-Paper Display App
     After=network.target

     [Service]
     User=pi
     WorkingDirectory=/home/pi/Desktop/project/e-Paper/RaspberryPi_JetsonNano/python/examples
     ExecStart=/usr/bin/python3 main.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

     Make sure to update the `WorkingDirectory` and `ExecStart` paths according to your actual Flask app location (`/home/pi/Desktop/project/e-Paper/RaspberryPi_JetsonNano/python/examples`) and Python interpreter (`/usr/bin/python3 main.py`).

2. **Move the Service File:**

   - Move the service file to the `/etc/systemd/system` directory using the following command:

     ```bash
     sudo mv e-paper-display-app.service /etc/systemd/system/
     ```

3. **Reload Systemd:**

   - Reload the systemd daemon to ensure it detects the new service file:

     ```bash
     sudo systemctl daemon-reload
     ```

4. **Start the Service:**

   - Start the Flask service using the following command:

     ```bash
     sudo systemctl start e-paper-display-app
     ```

   - This will start your Flask application as a daemon.

5. **Enable the Service:**

   - To automatically start the Flask service on system boot, enable the service:

     ```bash
     sudo systemctl enable e-paper-display-app
     ```

   - Now, your Flask application will start automatically whenever the system boots up.

6. **Check the Service Status:**

   - You can check the status of your Flask service using the following command:

     ```bash
     sudo systemctl status e-paper-display-app
     ```

   - This command will display the current status of the service and any error messages if present.

That's it! Your Flask application is now daemonized using the unique name "e-paper-display-app.service" and managed by `systemd`. You can start, stop, restart, and check the status of the service using `systemctl` commands.
