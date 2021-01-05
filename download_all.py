#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from groups import parse as get_groups
import datetime
import icalendar
import DateParser.get_events

GROUPS_PATH = "/root/BMSTU_Schedule/BMSTUScheduleAlisa/Groups/"

def download_schedule(group):
    path = GROUPS_PATH + group.upper() + "_TO_FIX.ics"
    fix_path = GROUPS_PATH + group.upper() + ".ics"

    os.system(str("bmstu-schedule " + group.upper() + " -o " + GROUPS_PATH))
    try:
        os.rename(fix_path, path)
    except FileNotFoundError:
        return
    with open(fix_path, "w") as wf:
        with open(path, "r") as f:
            for line in f:
                if (line.find("DTSTART") != -1 or line.find("DTEND") != -1):
                    wf.write(line[:-1:] + 'Z\n')
                else:
                    wf.write(line)

    os.remove(path)

    print(group + " downloaded")

    return True


if __name__ == "__main__":
    groups = get_groups()

    for group_name in groups:
        download_schedule(group_name)  # используем когда пользователь ввел название группы
