from spl.spiget import SpiGet


def add_parser_args(parser):
    parser.add_argument('query')


def run(args):
    spiget = SpiGet()
    results = spiget.resource_search(args.query)
    for result in results:
        print("{} - {}".format(result.name, result.tag))
    return 0
