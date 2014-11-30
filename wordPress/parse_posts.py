'''
Usage example:
python parse_posts.py http://imheavyinyourarms.wordpress.com
'''
import os
import re
import sys
import urllib
from hashlib import md5
from bs4 import BeautifulSoup


def parse(BASE_URL, pages=300):
    reload(sys)

    sys.setdefaultencoding('utf-8')

    posts = []
    titles = []
    for i in range(pages):

        #compose link
        url = BASE_URL + '/?paged=' + str(i)

        #get site in string
        string_website = urllib.urlopen(url).read().decode('latin-1', 'replace')

        #load page
        doc = BeautifulSoup(string_website, from_encoding='latin-1')
        if not doc:
            sys.exit(3)


        #find articles
        articles = doc.find_all("article") #, recursive=False)

        #if there are no articles end loop
        if not articles or doc.find(class_='error404'):
            if (i == 1):
                print('no articles on url %s' % (url))
            else:
                break


        #add new posts
        for x in articles:
            try:
                content = x.find(class_='entry-content').get_text()

                if x.h1.a.get_text() not in titles: #prevent duplicates

                    sharedaddy = x.find(class_='sharedaddy')
                    if (sharedaddy):
                        sharedaddy.decompose()
                    #content = content.get_text()
                    hexval = md5(content).hexdigest()
                    posts.append({
                        'id': x['id'],
                        'title': x.h1.a.get_text(),
                        'link': x.h1.a.get('href'),
                        'content': content,
                        'digest': hexval
                    })

                    titles.append(x.h1.a.get_text())
            except Exception, e:
                print(e)
                break

    return posts