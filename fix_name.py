#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

files = os.listdir("./Groups/")
for file_name in files:
    if file_name[-5] not in ['Б', 'М', 'А', 'Л']:
        print("./Groups/" + file_name + "-->" + "./Groups/" + file_name[:-4] + "Л.ics")
        os.rename("./Groups/" + file_name, "./Groups/" + file_name[:-4] + "Л.ics")
