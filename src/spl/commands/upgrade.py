from semantic_version import Version as SemVer
from spl.commands import delegate
from spl.commands.install import _do_install
from spl.errors import ExitCode
from spl.state import State, ResourceState


def add_parser_args(parser):
    parser.add_argument('package_name', nargs='?', default=None)


def run(spiget, args):
    with State.load(spiget) as state:
        if args.package_name:
            current = state.get_installed_resource(args.package_name)
            if current:
                return _upgrade_package(spiget, state, current)
            else:
                print("Resource {} is not installed.".format(args.package_name))
                return ExitCode.NOT_INSTALLED
        else:
            for resource in state.installed_resources.values():
                _upgrade_package(spiget, state, resource['resource'])
            return ExitCode.OK


def _is_newer_version(installed, latest):
    try:
        iv = SemVer(installed, partial=True)
        lv = SemVer(latest, partial=True)
        return lv > iv
    except:
        return False


def _upgrade_package(spiget, state, current):
    latest = spiget.resource_details(current.id)

    if _is_newer_version(current.current_version.name, latest.current_version.name):
        print("Upgrading {} from {} to {}".format(latest.name, current.current_version.name, latest.current_version.name))

        old_state = state.resource_state(current)

        delegate('disable', spiget, package_name=current.id)
        _do_install(state, latest)

        if old_state == ResourceState.INSTALLED_ENABLED:
            delegate('enable', spiget, package_name=current.id)
        else:
            print("Leaving resource {} disabled.".format(latest.name))

    return ExitCode.OK
