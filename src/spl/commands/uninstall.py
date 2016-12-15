from spl.commands import delegate
from spl.errors import ExitCode
from spl.state import State

import os
import shutil


def add_parser_args(parser):
    parser.add_argument('package_name')


def run(spiget, args):
    with State.load(spiget) as state:
        resource = state.get_installed_resource(args.package_name)

        if resource:
            delegate('disable', spiget, package_name=resource.id)

            plugins_dir = state.get_plugins_dir()
            source_jar_file = state.resource_jar_file(resource)
            spl_data_dir = os.path.join(plugins_dir, "{}-data".format(resource.id))

            print("Deleting {} and {}...".format(source_jar_file, spl_data_dir))

            try:
                os.unlink(source_jar_file)
            except FileNotFoundError:
                print("Could not find {} to delete it!".format(source_jar_file))
            shutil.rmtree(spl_data_dir)

            state.uninstall_resource(resource)

            print("{} uninstalled.".format(resource.name))

        else:
            print("Resource {} is not installed.".format(args.package_name))
            return ExitCode.NOT_INSTALLED
        return ExitCode.OK
