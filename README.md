# Create Alarm Clocker Using Python And SystemD
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/lbayfsj2tv233gwz5bg4.png)
## Python For Fun

- Make alarm clocker by using combine of systemD, python, and slackbot
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/h8i2ovhsmug5qi1n534c.png)
## **1. Create SystemD service**
- The service will start along with your machine and running background process to check clocker
```
⚡ $ cat Clocker.service 
[Unit]
Description=Polling check clocker alarm
Requires=network.target
After=multi-user.target

[Service]
Type=forking
PIDFile=/var/run/clocker_polling.pid
ExecStart=/opt/ops/clocker_polling.sh

StandardOutput=/var/log/clocker-alarm.log
StandardError=/var/log/clocker-alarm.error

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

## **2. Create wrapper script to start service**
```
⚡ $ cat /opt/ops/clocker_polling.sh 
#!/bin/bash
rm -f /var/run/clocker_polling.pid
python3 /opt/ops/clocker.py &
echo $! > /var/run/clocker_polling.pid

⚡ $ sudo chmod +x /opt/ops/clocker_polling.sh
```

## **3. Python script to run process**
```
⚡ $ cat /opt/ops/clocker.py 
import os
import requests
import time
from datetime import datetime
import json


class SlackWebHook:
    """ Send payload to slack """
    def __init__(self):
        self.webhook_url = 'https://hooks.slack.com/services/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'
        self.footer_icon = 'https://cdn2.iconfinder.com/data/icons/construction-2-15/65/65-512.png'
        self.slack_id = 'UU1111UU'

    def send_slack(self, msg):
        """ Send alarm to slack """
        color = '#750202'
        level = ':boom: ALERT :boom:'
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message = f"<@{self.slack_id}> {msg}"
        slack_payload = {"username": "Hurry-up",
                         "attachments": [{"fallback": "Required plain-text summary of the attachment.",
                                          "pretext": level,
                                          "color": color,
                                          "text": message,
                                          "footer": curr_time,
                                          "footer_icon": self.footer_icon}]}
        requests.post(self.webhook_url, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    while 1:
        now = datetime.now()
        if now.hour == 23 and now.minute == 3:
            slack = SlackWebHook()
            slack.send_slack("*Report to the boss now!!!*")
            time.sleep(5)
        else:
            time.sleep(15)
```

## **4. Start service**
```
⚡ $ sudo cp Clocker.service /lib/systemd/system/
⚡ $ systemctl start Clocker.service
⚡ $ systemctl status Clocker.service
● Clocker.service - Polling check clocker alarm
     Loaded: loaded (/lib/systemd/system/Clocker.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2020-12-27 22:04:31 +07; 57min ago
    Process: 99372 ExecStart=/opt/ops/clocker_polling.sh (code=exited, status=0/SUCCESS)
   Main PID: 99379 (python3)
      Tasks: 1 (limit: 18998)
     Memory: 16.9M
     CGroup: /system.slice/Clocker.service
             └─99379 python3 /opt/ops/clocker.py

Dec 27 22:04:31 jackdao systemd[1]: Starting Polling check clocker alarm...
Dec 27 22:04:31 jackdao systemd[1]: Started Polling check clocker alarm.
```

## **5. Enjoy!**
- The service will send slack message to your slack-channel at 23:03 every day 
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/4s8vannrzb5pux85uone.png)
