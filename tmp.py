# import sched, time
# s = sched.scheduler(time.time, time.sleep)
# def print_time(a='default'):
#     print("From print_time", time.time(), a)
#
# def print_some_times():
#     print(time.time())
#     s.enter(10, 1, print_time)
#     s.enter(5, 2, print_time, argument=('positional',))
#     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
#     s.run()
#     print(time.time())
#
# print_some_times()
import time, datetime

nt = datetime.datetime.now()

print(nt.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日'))
"%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}".format(Y='年', m='月', d='日', H='时', M='分', S='秒')