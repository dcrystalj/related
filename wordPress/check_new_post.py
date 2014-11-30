#save new posts
from __future__ import print_function

import sys
from hashlib import md5
from bs4 import BeautifulSoup
from reccommend_db import *
from parse_posts import *



def check_new_post(blog):
    posts = parse(blog, 1)

    try:
        for post in posts:
            p = Reccommend.get(Reccommend.post_id == post['id'])
            if (p.digest != md5(post['content']).hexdigest()):
                raise Exception
    except Exception, e:
        return "yes new blog post"

    return 'nope, nothing new'


blog = sys.argv[1]
print(check_new_post(blog))
