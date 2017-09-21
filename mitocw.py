import requests, bs4, re
from . import Platform, Course

class MitOCW(Platform):

    name = 'Mit OpenCourseWare'

    def _urls(self):
        base = 'https://ocw.mit.edu'
        res = requests.get(base + '/courses/audio-video-courses/')
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        anchor_elements = soup.select('.courseList td a')[1::3]
        link_dict = anchors_to_dict(anchor_elements)
        urls = [base + url for url in remove_versions(link_dict)]

        return urls

    def _parse(self, url):

        res = requests.get(url)
        
        if res.status_code != 404:
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            
            title = soup.select('h1.title')[0].text
            description = '\n'.join([p.text for p in soup.select('#description h2 ~ p')])

            topics = [a.text for a in soup.select('#related ul li a')]
            tags = [tag for topic in topics for tag in topic.split(' > ')]

            partners = ['OCW Scholar'] if soup.select('.reveal1') else []

            course = Course(title, partners, self.name, description, tags, url)
            return [course]

def anchors_to_dict(anchors):
    _dict = {}
    for a in anchors:
        _dict[strip_whitespace(a.text)] = a.get('href')
    return _dict

def strip_whitespace(text):
    return text.strip().replace('\n', ' ').replace('\t', ' ')

def remove_versions(link_dict):
    versions = {}
    urls = []

    regex = re.compile(r'(.*)\((Spring|Fall) (2\d{3})\)')
    for key in link_dict:
        match = regex.match(key)
        if match:
            course, _, year = match.groups()
            versions.setdefault(course, {})
            versions[course][year] = link_dict[key]
        else:
            urls.append(link_dict[key])

    for course in versions:
        latest_year = sorted(versions[course], reverse=True)[0]
        urls.append(versions[course][latest_year])
        
    return urls


        




