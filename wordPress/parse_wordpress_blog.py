import sys
import MySQLdb as mdb
import peewee
from peewee import *
from parse_posts import parse

reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLDatabase(sys.argv[2], user='root', passwd='root')

class Wpposts(peewee.Model):
    post_content=peewee.TextField()
    post_title = peewee.CharField()
    post_name = post_title

    class Meta:
        database = db

blog = sys.argv[1]
posts = parse(blog)

#remove duplicates
p = []
for k, i in enumerate(posts):
    for j in posts:
        if i['id'] != j['id'] and (i['digest'] == j['digest'] or i['title'] == j['title']):
            posts.pop(k)

for p in posts:
    Wpposts.create(post_content=p['content'], post_title=p['title'], post_name=p['title'])

print('done')
