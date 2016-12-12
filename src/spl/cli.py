#!/usr/bin/env python
# encoding: utf-8

import sys
import spl.commands as commands

from argparse import ArgumentParser
from spl.metadata import NAME, VERSION


COMMANDS = [c for c in dir(commands) if c[0] != "_" and callable(getattr(commands, c))]


def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    parser = ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version="{} v{}".format(NAME, VERSION))
    parser.add_argument("command", metavar="COMMAND", choices=COMMANDS)

    # Process arguments
    args, extras = parser.parse_known_args()

    if args.command in COMMANDS:
        return getattr(commands, args.command)(args, extras)
    else:
        # argparse should prevent us from getting here
        print("Unrecognised action: {}".format(args.command))
        print("Available actions: {}".format(COMMANDS))
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
