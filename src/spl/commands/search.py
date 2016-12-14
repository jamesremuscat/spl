from spl.spiget import SpiGet
from spl.errors import ExitCode


def add_parser_args(parser):
    parser.add_argument('query')


def run(args):
    spiget = SpiGet()
    results = spiget.resource_search(args.query)
    for result in results:
        print("{:<8} {} - {}".format(result.id, result.name, result.tag))
    return ExitCode.OK
