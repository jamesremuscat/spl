import requests


class SpiGet(object):
    def __init__(self):
        self.session = requests.Session()
        self.rootURL = "https://api.spiget.org/v2/"
        self.session.headers['User-Agent'] = "spl v0.0.1-dev"

    def resourceDetails(self, resourceIdent):
        result = self.session.get(self.rootURL + "resources/{}".format(resourceIdent))
        result.raise_for_status()
        return Resource(self, result.json())

    def author(self, authorID):
        result = self.session.get(self.rootURL + "authors/{}".format(authorID))
        result.raise_for_status()
        return Author(self, result.json())


class Resource(object):
    def __init__(self, spiget, json):
        self.spiget = spiget

        self.id = json['id']
        self.name = json['name']
        self.tag = json['tag']
        self.update_date = json['updateDate']
        self.author = spiget.author(json['author']['id'])
        self.downloads = json['downloads']
        self.links = json['links']
        self.version = json['version']
        self.versions = []
        # Iterate through all the versions available and append it to the objects available versions
        for version in json['versions']:
            self.versions.append(version)

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
