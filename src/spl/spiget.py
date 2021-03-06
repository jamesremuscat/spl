import cfscrape
import collections
import datetime
import requests
import spl.metadata as metadata


from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from spl.errors import NonSingletonResultException, NotDownloadableException


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
        if isinstance(json, collections.Sequence):
            raise NonSingletonResultException()
        self.id = json['id']
        self.name = json['name']
        self.tag = json['tag']
        self.update_date = datetime.datetime.fromtimestamp(json['updateDate'])

        if isinstance(json['author'], Author):
            self.author = json['author']
        else:
            self.author = spiget.author(json['author']['id'])

        if isinstance(json['versions'][0], Version):
            self.versions = json['versions']
        else:
            self.versions = sorted(spiget.resource_versions(self.id), key=lambda v: v.release_date, reverse=True)

        for v in self.versions:
            v.resource_id = self.id

        if isinstance(json['version'], Version):
            self.current_version = json['version']
            self.current_version.resource_id = None
        else:
            self.current_version = [v for v in self.versions if v.id == json['version']['id']][0]

        if isinstance(json['category'], Category):
            self.category = json['category']
        else:
            self.category = spiget.category(json['category']['id'])

        self.tested_versions = json['testedVersions']

        self.external = json['external']

        self.file_size = ""
        if not self.external:
            self.file_size = json['file']['size']

    def download(self):
        if not self.external:
            return requests.get("https://api.spiget.org/v2/resources/{}/download".format(self.id), stream=True)
        elif hasattr(self.current_version, 'url'):
            scraper = cfscrape.create_scraper()
            return scraper.get("https://www.spigotmc.org/{}".format(self.current_version.url), stream=True)
        else:
            raise NotDownloadableException()

    def for_json(self):
        return {
            'type': 'spl.spiget.Resource',
            'id': self.id,
            'name': self.name,
            'tag': self.tag,
            'updateDate': self.update_date.timestamp(),
            'author': self.author,
            'category': self.category,
            'versions': self.versions,
            'version': self.current_version,
            'testedVersions': self.tested_versions,
            'external': self.external,
            'file': {'size': self.file_size}
        }


class Author(object):
    def __init__(self, spiget, json):
        self.name = json['name']
        self.id = json['id']

    def for_json(self):
        return {
            'type': 'spl.spiget.Author',
            'id': self.id,
            'name': self.name
        }


class Category(object):
    def __init__(self, spiget, json):
        self.name = json['name']
        self.id = json['id']

    def for_json(self):
        return {
            'type': 'spl.spiget.Category',
            'name': self.name,
            'id': self.id
        }


def ListResult(clazz):
    class ListResultInner(object):
        def __init__(self, spiget, json):
            self.items = list(map(lambda v: clazz(self, v), json))

        def __getitem__(self, key):
            return self.items.__getitem__(key)

        def for_json(self):
            return self.items

    return ListResultInner


class Version(object):
    def __init__(self, spiget, json):
        self.id = json['id']
        self.name = json['name']
        self.release_date = datetime.datetime.fromtimestamp(json['releaseDate'])
        if 'url' in json:
            self.url = json['url']
        self.resource_id = None

    def download(self):
        if self.resource_id:
            scraper = cfscrape.create_scraper()
            return scraper.get("https://api.spiget.org/v2/resources/{}/versions/{}/download".format(self.resource_id, self.id), stream=True)
        else:
            raise NotDownloadableException()

    def __repr__(self, *args, **kwargs):
        return self.name

    def for_json(self):
        return {
            'type': 'spl.spiget.Version',
            'id': self.id,
            'name': self.name,
            'releaseDate': self.release_date.timestamp(),
            'url': self.url if hasattr(self, "url") else None
        }


class SearchResult(object):
    def __init__(self, spiget, json):
        self.name = json['name']
        self.tag = json['tag']
        self.id = json['id']


class SpiGet(object):
    def __init__(self):
        session = requests.Session()
        self.rootURL = "https://api.spiget.org/v2/"
        session.headers['User-Agent'] = "{} v{}".format(metadata.NAME, metadata.VERSION)

        self.session = CacheControl(
            session,
            cache=FileCache('.spl/cache')
        )

    author = api_call("authors/{}", Author)
    category = api_call("categories/{}", Category)

    resource_details = api_call("resources/{}", Resource)
    resource_versions = api_call("resources/{}/versions", ListResult(Version))

    resource_search = api_call("search/resources/{}", ListResult(SearchResult))
