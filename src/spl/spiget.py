import datetime
import requests

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


def api_call(url, clazz):
    def innerfunc(self, api_id):
        result = self.session.get(self.rootURL + url.format(api_id))
        result.raise_for_status()
        cum_result = result.json()
        if "X-Page-Count" in result.headers:
            while result.headers['X-Page-Count'] != result.headers['X-Page-Index']:
                cur_page = int(result.headers['X-Page-Index'])
                result = self.session.get(self.rootURL + url.format(api_id) + "?page={}".format(cur_page + 1))
                result.raise_for_status()
                cum_result += result.json()
        return clazz(self, cum_result)
    return innerfunc


class Resource(object):
    def __init__(self, spiget, json):
        self.spiget = spiget

        self.id = json['id']
        self.name = json['name']
        self.tag = json['tag']
        self.update_date = datetime.datetime.fromtimestamp(json['updateDate'])
        self.author = spiget.author(json['author']['id'])
        self.downloads = json['downloads']
        self.links = json['links']

        self.versions = sorted(spiget.resource_versions(self.id), key=lambda v: v.release_date, reverse=True)
        self.current_version = [v for v in self.versions if v.id == json['version']['id']][0]

        self.category_id = json['category']['id']
        self.external = json['external']

        self.file_size = ""
        if not self.external:
            self.file_size = json['file']['size']


class Author(object):
    def __init__(self, spiget, json):
        self.spiget = spiget
        self.name = json['name']
        self.id = json['id']


class Versions(object):
    def __init__(self, spiget, json):
        self.spiget = spiget
        self.versions = list(map(lambda v: Version(self, v), json))

    def __getitem__(self, key):
        return self.versions.__getitem__(key)


class Version(object):
    def __init__(self, spiget, json):
        self.spiget = spiget
        self.id = json['id']
        self.name = json['name']
        self.release_date = json['releaseDate']
        self.url = json['url']

    def __repr__(self, *args, **kwargs):
        return self.name


class SpiGet(object):
    def __init__(self):
        session = requests.Session()
        self.rootURL = "https://api.spiget.org/v2/"
        session.headers['User-Agent'] = "spl v0.0.1-dev"

        self.session = CacheControl(
            session,
            cache=FileCache('.spl/cache')
        )

    resourceDetails = api_call("resources/{}", Resource)
    resource_versions = api_call("resources/{}/versions", Versions)

    author = api_call("authors/{}", Author)
