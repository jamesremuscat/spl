from spl.errors import ExitCode
from spl.state import State, ResourceState


def add_parser_args(parser):
    pass  # No arguments


def run(spiget, args):
    with State.load(spiget) as state:

        print("\033[1m{:<8} {:<42} {:<10} {:<10}\033[0;0m".format(
            "ID",
            "Name",
            "Installed",
            "Latest"
        ))

        for installed_resource in state.installed_resources.values():
            latest_resource = spiget.resource_details(installed_resource['resource'].id)
            print_resource_details(installed_resource, latest_resource)

    return ExitCode.OK


def print_resource_details(installed, latest):
    print("{:<8} {:<42} {:<10} {:<10}".format(
        installed['resource'].id,
        "({})".format(installed['resource'].name) if installed['state'] == ResourceState.INSTALLED_DISABLED else installed['resource'].name,
        installed['resource'].current_version.name,
        latest.current_version.name
    ))
