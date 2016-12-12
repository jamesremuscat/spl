#!/usr/bin/env python
# encoding: utf-8

import sys

from argparse import ArgumentParser
from spl.metadata import NAME, VERSION


def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        parser = ArgumentParser()
        parser.add_argument('-V', '--version', action='version', version="{} v{}".format(NAME, VERSION))

        # Process arguments
        args = parser.parse_args()

        print(args)

        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0

    except Exception as e:

        sys.stderr.write(NAME + ": " + repr(e) + "\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
