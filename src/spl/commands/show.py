from spl.spiget import SpiGet


def add_parser_args(parser):
    parser.add_argument("package_name")


def run(args):
    spiget = SpiGet()
    print(formatResource(spiget.resourceDetails(args.package_name)))
    return 0


def formatResource(resource):
    strings = [
        "Package: {}".format(resource.name),
        "Author:  {}".format(resource.author.name),
        "Versions:  {}".format(resource.versions[0:5])
    ]

    return "\n".join(strings)
