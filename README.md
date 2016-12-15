= spl - Spigot Plugin Loader

`spl` is a command-line plugin manager for Spigot/Bukkit, written in Python 3.

== Usage examples

```
$ spl search broadcast
219      SimpleBroadcast - Very simple and lightweight broadcasting plugin with customizable prefix.
736      SimpleBroadcaster - Broadcast messages!
1517     YourAutoBroadcaster - Customize Your Own Messages To Be Broadcasted To Your Server!
1904     BungeeBroadCaster - Add a nice BroadCaster Plugin to your BungeeCord Server
...
```

```
$ spl install BungeeBroadCaster
Downloading resources/bungeebroadcaster.1904/download?version=6885 to .spl/plugins/1904.jar
Downloaded 6.03 kB.
Enabling plugin BungeeBroadCaster (1.1)...
```

```
$ spl show BungeeBroadCaster
Package:           BungeeBroadCaster
ID:                1904
Author:            emachinesg627
Tag:               Add a nice BroadCaster Plugin to your BungeeCord Server
Category:          Chat
Latest version:    1.1
Installed version: 1.1
Versions:          [1.1, 1.0]
Updated:           2014-11-28 16:49:00
Tested against:    []
```

== Installation

From PyPI:

```
pip install spl
```

Or from a GitHub checkout:

```
python setup.py install
```

== Commands Quick Reference

- `search` - search for a resource
- `show` - give details of a resource, either installed or not
- `install` - download, install and enable a plugin resource
- `enable` - enable an installed but disabled plugin
- `disable` - disable, but leave installed, a plugin
- `list` - lists all installed plugins and their current state/most recent version

Note to Minecraft server admin veterans: these are intended to be run from the commandline, not from within the MC server console!

== Todo

- `upgrade` - upgrade a single plugin, or all plugins, to their most recent version
- `uninstall` - completely remove a plugin and its data
- Allow specifying a particular version of a plugin to install
- Allow filters on searches
- Server-side plugin management extension (change plugin state without restart)
- Cache management (e.g. clear cache)

== Contributions

Contributions are welcome:

- Feature requests and bug reports: please raise an issue on GitHub
- Pull requests very welcome
