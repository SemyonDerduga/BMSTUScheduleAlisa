#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import icalendar
import DateParser.get_events


def download_schedule(group):
    
    path = "./Groups/"+group.upper()+"_TO_FIX.ics"
    fix_path = "./Groups/"+group.upper()+".ics"
    
    os.system(str("bmstu-schedule "+group.upper()+" -o ./Groups"))
    os.rename(fix_path, path)
    with open(fix_path, "w") as wf:
        with open(path, "r") as f:
            for line in f:
                if(line.find("DTSTART") != -1 or line.find("DTEND") != -1):
                    wf.write(line[:-1:]+'Z\n')
                else:
                    wf.write(line)

    os.remove(path)
    
    print(group + " downloaded")
    
    return True

            
        
groups = ["СМ3-92","СМ3-93","СМ3-111","СМ3-112","СМ3-113","СМ4-11","СМ4-12","СМ4-13","СМ4-31","СМ4-32","СМ4-51","СМ4-52","СМ4-71","СМ4-72","СМ4-91","СМ4-92","СМ4-111","СМ4-112","СМ4-113","СМ5-11","СМ5-11Б","СМ5-12Б","СМ5-11М","СМ5-12М","СМ5-13М","СМ5-31","СМ5-31Б","СМ5-32Б","СМ5-31М","СМ5-32М","СМ5-33М","СМ5-53","СМ5-51Б","СМ5-52Б","СМ5-71Б","СМ5-72Б","СМ6-11","СМ6-12","СМ6-13","СМ6-31","СМ6-32","СМ6-33","СМ6-51","СМ6-52","СМ6-71","СМ6-72","СМ6-91","СМ6-92","СМ6-93","СМ6-111","СМ6-112","СМ6-113","СМ7-11Б","СМ7-12Б","СМ7-13Б","СМ7-14Б","СМ7-11М","СМ7-12М","СМ7-13М","СМ7-31Б","СМ7-32Б","СМ7-33Б","СМ7-34Б","СМ7-31М","СМ7-32М","СМ7-33М","СМ7-51Б","СМ7-52Б","СМ7-53Б","СМ7-54Б","СМ7-55Б","СМ7-71Б","СМ7-72Б","СМ7-73Б","СМ7-74Б","СМ7-75Б","СМ8-11","СМ8-12","СМ8-31","СМ8-32","СМ8-51","СМ8-52","СМ8-59","СМ8-71","СМ8-72","СМ8-73","СМ8-74","СМ8-79","СМ8-91","СМ8-92","СМ8-93","СМ8-99","СМ8-111","СМ8-112","СМ8-113","СМ8-114","СМ8-119","СМ9-11","СМ9-12","СМ9-11М","СМ9-31","СМ9-32","СМ9-31М","СМ9-51","СМ9-52","СМ9-71","СМ9-72","СМ9-91","СМ9-92","СМ9-111","СМ9-112","СМ10-11","СМ10-12","СМ10-11М","СМ10-31","СМ10-32","СМ10-31М","СМ10-51","СМ10-52","СМ10-71","СМ10-72","СМ10-91","СМ10-92","СМ10-111","СМ10-112","СМ11-11Б","СМ11-11М","СМ11-31Б","СМ11-31М","СМ11-51Б","СМ11-71Б","СМ12-11","СМ12-11М","СМ12-31","СМ12-31М","СМ12-51","СМ12-71","СМ12-91","СМ12-111","СМ12-119","СМ13-11Б","СМ13-12Б","СМ13-11М","СМ13-12М","СМ13-13М","СМ13-31Б","СМ13-32Б","СМ13-31М","СМ13-32М","СМ13-33М","СМ13-34М","СМ13-51Б","СМ13-52Б","СМ13-71Б","ФН1-11Б","ФН1-11М","ФН1-31Б","ФН1-31М","ФН1-51Б","ФН2-11Б","ФН2-12Б","ФН2-12М","ФН2-31Б","ФН2-32Б","ФН2-31М","ФН2-32М","ФН2-51Б","ФН2-52Б","ФН2-71Б","ФН2-72Б","ФН4-11Б","ФН4-12Б","ФН4-11М","ФН4-12М","ФН4-13М","ФН4-31Б","ФН4-32Б","ФН4-31М","ФН4-32М","ФН4-33М","ФН4-51Б","ФН4-52Б","ФН4-71Б","ФН4-72Б","ФН11-11Б","ФН11-12Б","ФН11-13Б","ФН11-11М","ФН11-31Б","ФН11-32Б","ФН11-33Б","ФН11-31М","ФН11-51Б","ФН11-52Б","ФН11-53Б","ФН11-71Б","ФН11-72Б","ФН12-11Б","ФН12-11М","ФН12-31Б","ФН12-31М","ФН12-51Б","ФН12-71Б","Э1-11","Э1-12","Э1-13","Э1-31","Э1-32","Э1-33","Э1-51","Э1-52","Э1-53","Э1-71","Э1-72","Э1-91","Э1-92","Э1-99","Э1-111","Э1-112","Э1-119","Э2-11Б","Э2-12Б","Э2-11М","Э2-12М","Э2-31Б","Э2-32Б","Э2-31М","Э2-32М","Э2-51Б","Э2-52Б","Э2-71Б","Э2-72Б","Э3-11","Э3-12","Э3-19","Э3-31","Э3-32","Э3-51","Э3-52","Э3-59","Э3-71","Э3-72","Э3-79","Э3-91","Э3-92","Э3-99","Э3-111","Э3-112","Э3-119","Э4-11","Э4-11Б","Э4-12Б","Э4-11М","Э4-12М","Э4-13М","Э4-14М","Э4-15М","Э4-31","Э4-31Б","Э4-32Б","Э4-31М","Э4-32М","Э4-33М","Э4-34М","Э4-35М","Э4-51","Э4-54","Э4-52Б","Э4-53Б","Э4-71","Э4-72Б","Э4-73Б","Э4-91","Э4-111","Э5-11","Э5-11Б","Э5-11М","Э5-12М","Э5-13М","Э5-31","Э5-31Б","Э5-31М","Э5-32М","Э5-33М","Э5-51","Э5-52Б","Э5-71","Э5-72Б","Э5-91","Э5-111","Э6-11Б","Э6-11М","Э6-12М","Э6-31Б","Э6-31М","Э6-32М","Э6-51Б","Э6-52Б","Э6-71Б","Э7-11","Э7-12","Э7-31","Э7-32","Э7-51","Э7-52","Э7-71","Э7-72","Э7-91","Э7-92","Э7-111","Э7-112","Э7-113","Э8-11","Э8-11Б","Э8-12Б","Э8-11М","Э8-12М","Э8-31","Э8-31Б","Э8-32Б","Э8-31М","Э8-32М","Э8-51","Э8-52Б","Э8-53Б","Э8-71","Э8-72Б","Э8-91","Э8-111","Э9-11Б","Э9-12Б","Э9-11М","Э9-12М","Э9-13М","Э9-14М","Э9-31Б","Э9-32Б","Э9-31М","Э9-32М","Э9-33М","Э9-34М","Э9-35М","Э9-51Б","Э9-52Б","Э9-53Б","Э9-71Б","Э9-72Б","Э9-73Б","Э10-11Б","Э10-12Б","Э10-11М","Э10-12М","Э10-31Б","Э10-32Б","Э10-31М","Э10-32М","Э10-51Б","Э10-52Б","Э10-71Б","Э10-72Б","ЮР-11","ЮР-12","ЮР-13","ЮР-14","ЮР-11М","ЮР-31","ЮР-32","ЮР-33","ЮР-34","ЮР-35","ЮР-51","ЮР-52","ЮР-53","ЮР-54","ЮР-55","ЮР-71","ЮР-72","ЮР-73","ЮР-74","ЮР-91","ЮР-92","ЮР-93"]


if __name__ == "__main__":

    for group_name in groups:
        download_schedule(group_name) #используем когда пользователь ввел название группы

    #download_schedule("ИУ3-71Б") #используем когда пользователь ввел название группы
    