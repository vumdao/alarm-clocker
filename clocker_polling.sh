#!/bin/bash
rm -f /var/run/clocker_polling.pid
python3 /opt/ops/clocker.py &
echo $! > /var/run/clocker_polling.pid
