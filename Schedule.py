import os
import datetime
import icalendar
import DateParser.get_events
import subprocess


# from icalendar import Calendar, Event


def bash_command(cmd):
    subprocess.Popen(cmd, executable='/bin/bash')


# bash_command('a="Apples and oranges" && echo "${a/oranges/grapes}"')


def download_schedule(group):
    path = "./Groups/" + group.upper() + "_TO_FIX.ics"
    fix_path = "./Groups/" + group.upper() + ".ics"

    os.system(str("bmstu-schedule " + group.upper() + " -o ./Groups"))
    os.rename(fix_path, path)
    with open(fix_path, "w") as wf:
        with open(path, "r") as f:
            for line in f:

                if (line.find("DTSTART") != -1 or line.find("DTEND") != -1):
                    wf.write(line[:-1:] + 'Z\n')
                    continue
                wf.write(line)
    os.remove(path)
    return True


def get_time_first_lesson(group, date):
    day_scedule = DateParser.get_events.get_events(group, date)

    response = str(day_scedule[0][0]).split(" ")[1]
    return response


def get_schedule_by_date(group, date):
    response = ""
    day_scedule = DateParser.get_events.get_events(group, date)
    for lesson in day_scedule:
        response += '{} {} в {}, потом '.format(lesson[1], lesson[2], lesson[3]).replace("(сем)", "семинар").replace("(лек)", "лекция")
    if response:
        response += 'можешь идти домой!'
    else:
        return "Пар нет!"
    return response


if __name__ == "__main__":
    # download_schedule("ИУ3-71Б") #используем когда пользователь ввел название группы
    for lesson in get_schedule_by_date("ИУ3-71Б", "2018-11-27"):
        print(lesson)
