import requests, json, bs4, urllib.parse, math
from . import Course, Platform

class Edx(Platform):

    name = 'edX'
    
    def _urls(self):
        res = requests.get(make_url())
        
        count = json.loads(res.text)['objects']['count']
        num_pages = math.ceil(count / 20)

        urls = [make_url(page=page) for page in range(1, num_pages + 1)]
        
        return urls

    def _parse(self, url):
        res = requests.get(url)

        courses = []
        results = res.json()['objects']['results']
        for result in results:
            title = result['title']

            if result['full_description']:
                description = html_to_text(result['full_description'])
            else:
                description = result['short_description']
            
            snippet = ''
            if result['short_description'] and result['short_description'] != '.':
                snippet = result['short_description']
            
            url = result['marketing_url']
            tags = [subject_uuids.get(uuid) for uuid in result['subject_uuids']]
            partners = [result.get('org')]

            course = Course(title, partners, self.name,
                            description, tags, url, snippet=snippet)
            
            courses.append(course)

        return courses

subject_uuids = {'d8244ef2-45fb-4be3-a9d7-a6749cee3b19': 'Architecture',
                 '2cc66121-0c07-407b-96c4-99305359a36f': 'Art & Culture',
                 '9d5b5edb-254a-4d54-b430-776f1f00eaf0': 'Biology & Life Sciences',
                 '409d43f7-ff36-4834-9c28-252132347d87': 'Business & Management',
                 'c5ec1f86-4e59-4273-8e22-ceec2b8d10a2': 'Chemistry',
                 '605bb663-a342-4cf3-b5a5-fee2f33f1642': 'Communication',
                 'e52e2134-a4e4-4fcb-805f-cbef40812580': 'Computer Science',
                 'a168a80a-4b6c-4d92-9f1d-4c235206feaf': 'Data Analysis & Statistics',
                 '34173fb0-fe3d-4715-b4e0-02a9426a873c': 'Design',
                 'bab458d9-19b3-476e-864f-8abd1d1aab44': 'Economics & Finance',
                 '8ac7a3da-a60b-4565-b361-384baaa49279': 'Education & Teacher Training',
                 '337dfb23-571e-49d7-9c8e-385120dea6f3': 'Electronics',
                 '07406bfc-76c4-46cc-a5bf-2deace7995a6': 'Energy & Earth Sciences',
                 '0d7bb9ed-4492-419a-bb44-415adafd9406': 'Engineering',
                 '8aaac548-1930-4614-aeb4-a089dae7ae26': 'Environmental Studies',
                 '8a552a20-963e-475c-9b0d-4c5efe22d015': 'Ethics',
                 'caa4db79-f325-41ca-8e09-d5bb6e148240': 'Food & Nutrition',
                 '51a13a1c-7fc8-42a6-9e96-6636d10056e2': 'Health & Safety',
                 'c8579e1c-99f2-4a95-988c-3542909f055e': 'Histroy',
                 '00e5d5e0-ce45-4114-84a1-50a5be706da5': 'Humanities',
                 '32768203-e738-4627-8b04-78b0ed2b44cb': 'Language',
                 '4925b67d-01c4-4287-a8d1-a3e0066113b8': 'Law',
                 '74b6ed2a-3ba0-49be-adc9-53f7256a12e1': 'Literature',
                 'a669e004-cbc0-4b68-8882-234c12e1cce4': 'Math',
                 'a5db73b2-05b4-4284-beef-c7876ec1499b': 'Medicine',
                 'f520dcc1-f5b7-42fe-a757-8acfb1e9e79d': 'Music',
                 '830f46dc-624e-46f4-9df0-e2bc6b346956': 'Philosophy & Ethics',
                 '88eb7ca7-2296-457d-8aac-e5f7503a9333': 'Physics',
                 'f830cfeb-bb7e-46ed-859d-e2a9f136499f': 'Science',
                 'eefb009b-0a02-49e9-b1b1-249982b6ce86': 'Social Sciences'}

def make_url(page=1):
    params = {'selected_facets[]': 'transcript_languages_exact:English',
              'partner': 'edx',
              'content_type[]': 'courserun',
              'page': page,
              'page_size': 20}

    return 'https://www.edx.org/api/v1/catalog/search?' + urllib.parse.urlencode(params)

def html_to_text(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    return soup.text
