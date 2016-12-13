from spl.spiget import SpiGet


def add_parser_args(parser):
    parser.add_argument("package_name")


def run(args):
    spiget = SpiGet()
    print(formatResource(spiget.resource_details(args.package_name)))
    return 0


def formatResource(resource):
    strings = [
        "Package:        {}".format(resource.name),
        "Author:         {}".format(resource.author.name),
        "Tag:            {}".format(resource.tag),
        "Category:       {}".format(resource.category.name),
        "Latest version: {}".format(resource.current_version),
        "Versions:       {}".format(resource.versions),
        "Updated:        {}".format(resource.update_date),
        "Tested against: [{}]".format(", ".join(resource.tested_versions))
    ]

    return "\n".join(strings)
