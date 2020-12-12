from .ics import *
import urllib.request
import datetime

def get_events(group, date):
    
    path = "./Groups/"+group+".ics"
    #datetime(date[0],date[1],date[2])
    #datetime_object = datetime.datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    
    with open(path) as f:
        ics_string = f.read()
    
    window_start = datetime.datetime.strptime(str(date+'-00-00-01-+0300'),'%Y-%m-%d-%H-%M-%S-%z')

    #window_start = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),timezone.utc)
    #window_start = datetime.datetime.now(timezone.utc)
    window_end = window_start + datetime.timedelta(seconds=86340)
    print("from time "+str(window_start)+"to finish time"+str(window_end))
    events = get_events_from_ics(ics_string, window_start, window_end)
    lessons = []
    for e in events:
        #if str(e['startdt']).split(" ")[0] == date:
        lessons.append([e['startdt'], e['desc'], e['summary'], e['loc']])
        #print('{};{};{};{}'.format(e['startdt'], e['desc'], e['summary'], e['loc']))
    return lessons


#print("|||".join(get_events("ИУ3-11Б","2018-11-15")))