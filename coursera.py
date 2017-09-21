import requests, json, math, urllib.parse
from . import Course, Platform

class Coursera(Platform):

    name = 'Coursera'

    def __init__(self):
        self.partner_ids = fetch_partners()

    def _urls(self):
        res = requests.get(make_url())

        total = json.loads(res.text)['paging']['total']
        num_pages = math.ceil(total / 100)

        urls = [make_url(100*page) for page in range(num_pages)]
        return urls

    def _parse(self, url):
        courses = []
        res = requests.get(url)

        elements = json.loads(res.text)['elements']
        for element in elements:
            if 'en' in element['primaryLanguages']:
                title = element['name']
                description = element['description']
                
                partners = [self.partner_ids.get(id) for id in element.get('partnerIds')]

                tags = []
                for domain in element['domainTypes']:
                    tags.append(domain['domainId'].replace('-', ' '))
                    tags.append(domain['subdomainId'].replace('-', ' '))

                url = 'https://www.coursera.org/learn/' + element['slug']

                course = Course(title, partners, self.name,
                                description, tags, url)

                courses.append(course)
        
        return courses
                    
def make_url(start=0):
    params = {'start': start,
              'limit': 100,
              'fields': ','.join(['name', 'description', 'partnerIds', 
                                  'slug', 'primaryLanguages', 'domainTypes'])
             }
    return 'https://api.coursera.org/api/courses.v1?' + urllib.parse.urlencode(params)

def fetch_partners():
    uri = 'https://api.coursera.org/api/partners.v1'
    res = requests.get(uri)
    elements = json.loads(res.text)['elements']

    partner_ids = {}
    for element in elements:
        partner_ids[element['id']] = element['name']

    return partner_ids

    


