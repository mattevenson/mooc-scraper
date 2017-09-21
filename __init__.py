from multiprocessing import Pool

class Course:
    
    def __init__(self, title, partners, platform, 
                 description, tags, url, snippet=''):
        self.title = title
        self.partners = partners
        self.platform = platform
        self.description = description
        self.tags = tags
        self.url = url

        if snippet:
            self.snippet = snippet
        else:
            self.snippet = description.split('.')[0] + '.'

    def _dict(self):
        return {'title': self.title,
                'partners': self.partners,
                'platform': self.platform,
                'snippet': self.snippet,
                'description': self.description,
                'tags': self.tags,
                'url': self.url}

class Platform:

    name = ''
    
    def courses(self):
        pool = Pool(10)
        result_sets = pool.map(self._parse, self._urls())
        return flatten(result_sets)

    def _urls(self):
        raise NotImplementedError()

    def _parse(self, url):
        raise NotImplementedError()

def flatten(list):
    return [item for sublist in list for item in sublist]

from .edx import Edx
from .coursera import Coursera
from .udacity import Udacity
from .mitocw import MitOCW
from .futurelearn import FutureLearn