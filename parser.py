from urllib import request
from constants import (
    KARDACHI_TARASOVKA_LINK,
    TARASOVKA_KARDACHI_LINK,
    CURRENCY_LINK
)
import time

def _train_parser(link):
    lst = str(request.urlopen(link).read()
    ).split('<span class="_time">')
    lst = [str(i).split('</span>') for i in lst]

    array = [i[0] for i in lst
    if i[0][0].isdigit()
    and i[0][1].isdigit()]
    shedule = dict((
        str(array[i]),
        str(array[i+1]
    )) for i in range(0, len(array)-1, 2))

    return shedule

def nearest_parser(link):
    shedule = _train_parser(link)

    now = time.asctime(time.localtime()).split(' ')[4].split(':')
    now_mins = int(now[0])*60+int(now[1])

    times = {}
    for i, j in shedule.items():
        route_hours = int(float(i))
        route_minutes = float(i) - route_hours
        route_time = route_hours*60 + route_minutes*100
        times[str(i)] = route_time

    ans = [i for i, j in times.items() if j > now_mins]
    l = len(ans)
    ans = ans[:3] if l>=3 else ans[:2] if l==2 else ans
    l = len(ans)

    r1 = 'route'
    resp = f"  {l} {r1 + 's' if len(ans)>1 else r1} available\n"
    for i in ans:
        mins = _minute_stacker(times[str(i)]-now_mins)
        resp += i + "-"*4 + shedule[i] + f"-{mins} \n"

    return resp

def _minute_stacker(mins):
    mins_old = int(mins)
    mins = str(int(mins)) + ' minutes' if int(mins) <= 59 else f"{int(mins//60)} h"
    mins = mins + f" {mins_old-(mins_old//60)*60} m" if mins_old%60 != 0 and int(mins_old)>=59 else mins
    return mins


def currency_parser(link):
    lst = str(request.urlopen(link).read()
    ).split('<span>')
    lst = [str(i).split('</span>') for i in lst]
    for i in lst:
        if i[0][0].isdigit() and i[0][0] != '0':
            yield i[0]
