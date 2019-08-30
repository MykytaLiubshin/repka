from urllib import request
from constants import KARDACHI_TARASOVKA_LINK
import time

def train_parser(link):
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


a = train_parser(KARDACHI_TARASOVKA_LINK)
shedule = train_parser(KARDACHI_TARASOVKA_LINK)
now = time.asctime(time.localtime()).split(' ')[3].split(':')
now_mins = int(now[0])*60+int(now[1])
times = {}
for i, j in shedule.items():
    route_hours = int(float(i))
    route_minutes = float(i) - route_hours
    route_time = route_hours*60 + route_minutes
    times[str(i)] = route_time

ans = [i for i, j in times.items() if j > now_mins]
l = len(ans)
ans = ans[:3] if l>=3 else ans[:2] if l==2 else ans

r1 = 'route'
r2 = r1+'s'
resp = f"  {len(ans)} {r2 if len(ans)>1 else r1} available\n"

for i in ans:
    resp += i + "-"*12 + shedule[i] + '\n'


    
