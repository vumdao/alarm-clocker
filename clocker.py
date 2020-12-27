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
