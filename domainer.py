import time
import datetime
from sagemcom.sagemcomclient import Sagemcomclient
from domeneshop import Client
import os
import secrets

#MODEM_USER = secrets.MODEM_USER
#MODEM_PASSWORD = secrets.MODEM_PASSWORD
TOKEN = secrets.TOKEN
SECRET = secrets.SECRET
DOMAIN_ID = secrets.DOMAIN_ID
RECORD_ID = secrets.RECORD_ID

hostnames = [
    '123.123.123.132'
    '8.8.8.8',
    '195.88.55.16',
    '208.67.222.222',
    '1.1.1.1',
]

class Domainer():
    def __init__(self):
        self.token = TOKEN
        self.secret = SECRET
        self.domene_auth()

    def domene_auth(self):
        try:
            client = Client(self.token, self.secret)
        except:
            pass # TODO: wait for online and try again, if still error, write to log
        return client

    def domene_update(self, ip):
        client = self.domene_auth()
        record = client.get_record(DOMAIN_ID, RECORD_ID)
        record["data"] = ip
        del record["id"]
        client.modify_record(DOMAIN_ID, RECORD_ID, record)

    def auth_sagemcom(self):
        client = Sagemcomclient(secrets.MODEM_USER, secrets.MODEM_PASSWORD)
        client.login() # will raise an exception on login failed
        return client

    def get_ip_sagemcom(self):
        client = self.auth_sagemcom()
        query = client.get_values_tree('Device/DHCPv4/Clients')
        ip = query["parameters"]["value"][0]["IPAddress"]
        if self.send_pings():
            self.check_ip(ip)
        else:
            self.log_update("Offline")

    def get_ip(self):
        cmd = "curl ifconfig.me"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        ip = output.decode("ascii")
        if self.send_pings():
            self.check_ip(ip)
        else:
            self.log_update("Offline")

    def send_pings(self):
        for hostname in hostnames:
            response = os.system('ping -c 1 ' + hostname + ' > /dev/null 2>&1')
            if response == 0:
                return True
        return False

    def check_ip(self, current_ip):
        with open('/var/log/domainer/ip.log', 'r') as f:
            for line in f:
                pass
            last_line = line
        f.close()
        line = last_line.strip()
        entry = line.split(" ")
        previous_ip = entry[-1]
        if previous_ip != current_ip:
            self.update_ip(current_ip)

    def update_ip(self, current_ip):
        self.domene_update(current_ip)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        entry = time + " " + current_ip + "\n"
        with open('/var/log/domainer/ip.log', 'a') as f:
            f.write(entry)
            f.close()

    def log_update(self, entry):
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        entry = time + " " + entry + "\n"
        with open('/var/log/domainer/domainer.log', 'a') as f:
            f.write(entry)
            f.close()

if __name__ == "__main__":
    domainer = Domainer()
    domainer.get_ip()


