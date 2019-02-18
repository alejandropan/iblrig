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
import subprocess
import sys
from pathlib import Path

from setup_default_config import (copy_code_files_to_iblrig_params,
                                  update_pybpod_config)

IBLRIG_ROOT_PATH = Path.cwd()


def get_versions():
    vers = subprocess.check_output(
        "git ls-remote --tags origin".split()).decode().split()
    vers = [x for x in vers[1::2] if '{' not in x]
    vers = [x.split('/')[-1] for x in vers]
    available = [x for x in vers if x >= '3.0.0']
    print("\nAvailable versions: {}\n".format(available))
    return vers


def get_branches():
    branches = subprocess.check_output(
        "git ls-remote --heads origin".split()).decode().split()
    branches = [x.split('heads')[-1] for x in branches[1::2]]
    branches = [x[1:] for x in branches]
    print("\nAvailable branches: {}\n".format(branches))

    return branches


def get_current_branch():
    branch = subprocess.check_output(
        "git branch --points-at HEAD".split()).decode().strip().strip('* ')

    return branch


def get_current_version():
    tag = subprocess.check_output(["git", "tag",
                                   "--points-at", "HEAD"]).decode().strip()
    print("\nCurrent version: {}".format(tag))
    return tag


def pull(branch):
    subprocess.call(['git', 'pull', 'origin', branch])


def iblrig_params_path():
    return str(Path(os.getcwd()).parent / 'iblrig_params')


def import_tasks():
    if get_current_version() > '3.3.0' or get_current_branch() == 'develop':
        update_pybpod_config(iblrig_params_path())
    copy_code_files_to_iblrig_params(iblrig_params_path(),
                                     exclude_filename=None)


def checkout_version(ver):
    print("\nChecking out {}".format(ver))
    subprocess.call(["git", "reset", "--hard"])
    subprocess.call(['git', 'checkout', 'tags/' + ver])


def checkout_branch(branch):
    print("\nChecking out {}".format(branch))
    subprocess.call(['git', 'checkout', branch])
    subprocess.call(["git", "reset", "--hard"])
    pull(branch)


def checkout_single_file(file=None, branch='master'):
    subprocess.call("git checkout origin/{} -- {}".format(branch,
                                                          file).split())

    print("Checked out", file, "from branch", branch)


def update_remotes():
    subprocess.call(['git', 'remote', 'update'])


def update_ibllib():
    os.chdir(IBLRIG_ROOT_PATH.parent / 'ibllib')
    subprocess.call(["git", "reset", "--hard"])
    subprocess.call(["git", "pull"])
    os.chdir("./python")
    if 'ciso8601' not in os.popen("conda list").read().split():
        os.system(
            "conda activate iblenv && conda install -c conda-forge -y ciso8601")

    os.system("conda activate iblenv && pip install -e .")
    os.chdir(IBLRIG_ROOT_PATH)


def branch_info():
    print("Current availiable branches:")
    print(subprocess.check_output(["git", "branch", "-avv"]).decode())


def info():
    update_remotes()
    # branch_info()
    ver = get_current_version()
    versions = get_versions()
    if not ver:
        print("WARNING: You appear to be on an untagged release.",
              "\n         Try updating to a specific version")
        print()
    else:
        idx = sorted(versions).index(ver) if ver in versions else None
        if idx + 1 == len(versions):
            print("\nThe version you have checked out is the latest version\n")
        else:
            print("Newest version |{}| type:\n\npython update.py {}\n".format(
                sorted(versions)[-1], sorted(versions)[-1]))


if __name__ == '__main__':
    # TODO: Use argparse!!
    # If called alone
    if len(sys.argv) == 1:
        info()
    # If called with something in front
    elif len(sys.argv) == 2:
        versions = get_versions()
        branches = get_branches()
        help_args = ['-h', '--help', '?']
        # HELP
        if sys.argv[1] in help_args:
            print(__doc__)
        # UPDATE TO VERSION
        elif sys.argv[1] in versions:
            checkout_version(sys.argv[1])
            import_tasks()
            update_ibllib()
        elif sys.argv[1] in branches:
            checkout_branch(sys.argv[1])
            import_tasks()
            update_ibllib()
        # UPDATE IBLLIB
        elif sys.argv[1] == 'ibllib':
            update_ibllib()
        # UPDATE UPDATE
        elif sys.argv[1] == 'update':
            checkout_single_file(file='update.py', branch='master')
        # UPDATE REINSTALL
        elif sys.argv[1] == 'reinstall':
            os.system("conda deactivate && python install.py")
        # UNKNOWN COMMANDS
        else:
            print("ERROR:", sys.argv[1],
                  "is not a  valid command or version number.")
            raise ValueError
    # If called with something in front of something in front :P
    elif len(sys.argv) == 3:
        branches = get_branches()
        commands = ['update' 'ibllib']
        # Command checks
        if sys.argv[1] not in commands:
            print("ERROR:", "Unknown command...")
            raise ValueError
        if sys.argv[2] not in branches:
            print("ERROR:", sys.argv[2], "is not a valid branch.")
            raise ValueError
        if sys.argv[2] not in ['master', 'develop']:
            print("ERROR:", sys.argv[2], "is not a valid branch.")
            raise ValueError
        # Commands
        if sys.argv[1] == 'update' and sys.argv[2] in branches:
            checkout_single_file(file='update.py', branch=sys.argv[2])
        if sys.argv[1] == 'ibllib' and sys.argv[2] in ['master', 'develop']:
            checkout_single_file(file='update.py', branch=sys.argv[2])

    print("\n")
