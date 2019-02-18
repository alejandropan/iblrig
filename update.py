#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date:   2018-06-08 11:04:05
# @Last Modified by:   Niccolò Bonacchi
# @Last Modified time: 2018-07-12 17:10:22
"""
Usage:
    update.py
        Will fetch changes from origin. Nothing is updated yet!
        Calling update.py will display information on the available versions
    update.py -h | --help | ?
        Displays this docstring.
    update.py <version>
        Will checkout the <version> release and import task files to pybpod.
    update.py <branch>
        Will checkout the latest commit of <branch> and import task files to
        pybpod.
    update.py reinstall
        Will reinstall the rig to the latest revision on master.
    update.py ibllib
        Will reset ibllib to latest revision on master and install to iblenv.
    update.py update
        Will update itself to the latest revision on master.
    update.py update <branch>
        Will update itself to the latest revision on <branch>.
"""
import os
import sys


if __name__ == '__main__':
    os.system(f"activate iblenv && python update_code.py {''.join(sys.argv[1:])}")
