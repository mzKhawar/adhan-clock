import sys
from crontab import CronTab
from utils.enums import Path

cron = CronTab(user="mkhawar")
cron.remove_all()
daily = cron.new(command=f"{Path.VENV} {Path.BASE}/main.py")
daily.hour.on(0)
daily.minute.on(30)
cron.write()
sys.exit()
