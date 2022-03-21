#### Domene.shop updater

Setup is for a Sagemcom FAST3890V3 delivered by the ISP Get in Norway

##### Installation

    python3 -m venv domeneshop-updater
    source domeneshop-updater/bin/activate
    pip3 install -r requirements.txt

##### Crontab entry

	* * * * * python3 /opt/domainer/domainer.py >> /var/log/domainer/error.log 2>&1
