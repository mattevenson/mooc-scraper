import requests, bs4
from . import Course, Platform

class FutureLearn(Platform):

    name = 'FutureLearn'

    def _urls(self):
        base = 'https://www.futurelearn.com'

        res = requests.get(base + '/courses')
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        urls = []
        anchor_elements = soup.select('a.title')
        for element in anchor_elements:
            url = base + element.get('href')
            urls.append(url)

        return urls

    def _parse(self, url):
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        title = soup.select('h1')[0].text.strip()
        
        description = '\n'.join([p.text for p in soup.select('#section-overview p')])
        snippet = soup.select('h1 + p')[0].text

        partners = []
        org_images = soup.select('.m-dual-billboard .a-standard-org-logo a img')
        for image in org_images:
            partners.append(image.get('title'))
        
        tags = []
        category_links = soup.select('.run-related p.old-text-typescale a')
        for link in category_links:
            tag = link.text.replace('\xa0', ' ')
            tags.append(tag)

        course = Course(title, partners, self.name, 
                        description, tags, url, snippet=snippet)
        return [course]

