from spl.errors import ExitCode
from spl.state import State, ResourceState
from semantic_version import Version as SemVer


def add_parser_args(parser):
    pass  # No arguments


_TERMINAL_BOLD = "\033[1m"
_TERMINAL_NORMAL = "\033[0;0m"


def run(spiget, args):
    with State.load(spiget) as state:

        print("{}{:<8} {:<42} {:<10} {:<10}{}".format(
            _TERMINAL_BOLD,
            "ID",
            "Name",
            "Installed",
            "Latest",
            _TERMINAL_NORMAL
        ))

        for installed_resource in state.installed_resources.values():
            latest_resource = spiget.resource_details(installed_resource['resource'].id)
            print_resource_details(installed_resource, latest_resource)

    return ExitCode.OK


def print_resource_details(installed, latest):
    is_outdated = _is_newer_version(installed['resource'].current_version.name, latest.current_version.name)
    print("{:<8} {:<42} {:<10} {:<10}".format(
        installed['resource'].id,
        "({})".format(installed['resource'].name) if installed['state'] == ResourceState.INSTALLED_DISABLED else installed['resource'].name,
        installed['resource'].current_version.name,
        "{}{}{}".format(
            _TERMINAL_BOLD if is_outdated else "",
            latest.current_version.name,
            _TERMINAL_NORMAL if is_outdated else ""
        )
    ))


def _is_newer_version(installed, latest):
    try:
        iv = SemVer(installed, partial=True)
        lv = SemVer(latest, partial=True)
        return lv > iv
    except:
        return False
