import os
import yaml

from spl.errors import NonSingletonResultException, ExitCode
from spl.state import State, ResourceState
from zipfile import ZipFile


def add_parser_args(parser):
    parser.add_argument("package_name")


def run(spiget, args):
    with State.load(spiget) as state:
        try:
            resource = spiget.resource_details(args.package_name)

            if state.resource_state(resource) != ResourceState.NOT_INSTALLED:
                print("Resource {} is already installed, nothing to do.".format(resource.name))
                return ExitCode.OK

            if not hasattr(resource.current_version, 'url'):
                print("Resource {} ({}) is not installable (no URL supplied).".format(resource.name, resource.current_version.name))
                return ExitCode.UNINSTALLABLE

            plugins_dir = state.get_plugins_dir()
            dest_file = os.path.join(plugins_dir, args.package_name + ".jar")
            print("Downloading {} to {}".format(resource.current_version.url, dest_file))
            plugin_file = resource.download()
            size = 0
            with open(dest_file, 'wb') as dest:
                for chunk in plugin_file.iter_content(chunk_size=1024):
                    if chunk:
                        dest.write(chunk)
                        size += len(chunk)
            print("Downloaded {:.2f} kB.".format(size / 1024))

            state.install_resource(resource)

            print("Enabling plugin {} ({})...".format(resource.name, resource.current_version.name))

            data_dir_name = get_data_directory(dest_file)
            os.symlink(os.path.abspath(dest_file), 'plugins/{}.jar'.format(data_dir_name))
            os.mkdir(os.path.join(plugins_dir, data_dir_name))
            os.symlink(os.path.abspath(os.path.join(plugins_dir, data_dir_name)), 'plugins/{}'.format(data_dir_name))

            state.enable_resource(resource)

            return ExitCode.OK
        except NonSingletonResultException:
            print("'{}' matches more than one resource. Please use the resource ID to show details.".format(args.package_name))
            return ExitCode.NON_SINGLETON_RESULT


def get_data_directory(plugin_jar):
    with ZipFile(plugin_jar, 'r') as jar:
        with jar.open('plugin.yml', 'r') as plugin_yml:
            yml = yaml.load(plugin_yml)
            return yml['name']
