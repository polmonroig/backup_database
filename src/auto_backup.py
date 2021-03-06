#!/usr/bin/python3
from version import __version__
from parser import Parser
from database import ProjectDatabase
import os
import sys

def interactive(database):
    parser = Parser()
    exe = os.path.dirname(os.path.realpath(__file__))
    exe = exe.split('/')
    init_file = '/'
    for file in exe:
        init_file = os.path.join(init_file, file)
    init_file = os.path.join(init_file, '.config')
    for action in parser.read_file(init_file):
        database.interact(action)

    for action in parser.loop():
        database.interact(action)


def scripting(database):
    path = sys.argv[1]
    parser = Parser()
    for action in parser.read_file(path):
        database.interact(action)

def main():
    print('Backup utility', __version__)
    database = ProjectDatabase()
    if len(sys.argv) >= 2:
        scripting(database)
    else:
        interactive(database)


if __name__ == '__main__':
    main()
