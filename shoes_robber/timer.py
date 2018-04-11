import sched, time
from datetime import datetime

GLOBAL_scheduler = sched.scheduler(time.time, time.sleep)

target = datetime.strptime("2018-04-10 11:29:10", "%Y-%m-%d %H:%M:%S")
now = datetime.now()
delay = (target - now).total_seconds()


def call():
    print(datetime.now())


GLOBAL_scheduler.enter(1, 1, call)
GLOBAL_scheduler.enter(1 + 1, 1, call)
GLOBAL_scheduler.enter(1 + 2, 1, call)

GLOBAL_scheduler.run(blocking=False)

print("hello world")

while True:
    pass
