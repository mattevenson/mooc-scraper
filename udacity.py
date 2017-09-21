import requests, json
from markdown2 import markdown
from bs4 import BeautifulSoup
from . import Course, Platform

class Udacity(Platform):

    name = 'Udacity'

    def _urls(self):
        return ['https://www.udacity.com/public-api/v0/courses']

    def _parse(self, url):
        courses = []

        res = requests.get(url)
        objects = json.loads(res.text)['courses']
        for _object in objects:
            title = _object['title']
            description = markdown_to_text(_object['summary'])

            snippet = ''
            if _object['short_summary']:
                snippet = markdown_to_text(_object['short_summary'])

            tags = _object['tracks']
            partners = [affiliate['name'] for affiliate in _object['affiliates']]
            url = _object['homepage']

            course = Course(title, partners, self.name,
                            description, tags, url, snippet=snippet)

            courses.append(course)
        
        return courses

def markdown_to_text(md):
    return BeautifulSoup(markdown(md), 'lxml').text



