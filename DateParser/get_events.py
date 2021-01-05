from .ics import *
import urllib.request
import datetime

GROUPS_PATH = "/root/BMSTU_Schedule/BMSTUScheduleAlisa/Groups/"

def get_events(group, date):
    
    path = GROUPS_PATH+group+".ics"

    with open(path) as f:
        ics_string = f.read()
    
    window_start = datetime.datetime.strptime(str(date+'-00-00-01-+0300'),'%Y-%m-%d-%H-%M-%S-%z')

    window_end = window_start + datetime.timedelta(seconds=86340)
    print("from time "+str(window_start)+"to finish time"+str(window_end))
    events = get_events_from_ics(ics_string, window_start, window_end)
    lessons = []
    for e in events:
        lessons.append([e['startdt'], e['desc'], e['summary'], e['loc']])
    return lessons
