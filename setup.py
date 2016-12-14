from setuptools import setup, find_packages
import re

VERSIONFILE = "src/spl/metadata.py"
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^VERSION = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
except EnvironmentError:
    print("unable to find version in %s" % (VERSIONFILE,))
    raise RuntimeError("if %s exists, it is required to be well-formed" % (VERSIONFILE,))

setup(
    name='spl',
    version=verstr,
    description='Spigot/Bukkit Plugin Manager',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://github.com/jamesremuscat/spl',
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir = {'':'src'},
    setup_requires=['nose'],
    tests_require=[],
    install_requires=['bunch', 'cachecontrol[filecache]', 'cfscrape', 'lockfile', 'pyyaml', 'requests', 'simplejson'],
    entry_points={
        'console_scripts': [
            'spl = spl.cli:main',
            ],
        }
      )
