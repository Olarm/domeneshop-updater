#### Domene.shop updater

Setup is for a Sagemcom FAST3890V3 delivered by the ISP Get in Norway

##### Crontab entry

	* * * * * python3 /opt/domainer/domainer.py >> /var/log/domainer/error.log 2>&1
