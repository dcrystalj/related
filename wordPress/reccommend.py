#pass 466192d3
from __future__ import print_function
import copy
import csv
import re
import math
from collections import Counter
import parse_posts
import MySQLdb as mdb
import sys
import operator
import peewee
from peewee import *
import os
import re
import sys
import urllib
from hashlib import md5
from bs4 import BeautifulSoup
from reccommend_db import *
from filtertxt import filtertxt
from parse_posts import parse

reload(sys)
sys.setdefaultencoding('utf-8')

def frequency(string):
    """
    return dict of frequncy for each quadruple of letters
    """
    string = ["%s%s%s%s" %(string[i],string[i+1],string[i+2],string[i+3]) for i in range(len(string)-4)]
    return Counter(string)

def absoluteDist(a):
    a = sum(x*x for x in a.values())
    a = math.sqrt(a)
    return a

def dotProduct(x1,x2):
    return sum(v*x2.get(k,0) for k,v in x1.items())

def cosDist(a,b):
    x = absoluteDist(a)*absoluteDist(b)
    if(x>0):
        return 1-dotProduct(a,b)/x
    else:
        return 0

def sort_distances(posts, distances, post):
    txt = '{'
    dict_posts = {}
    for i in posts:
        dict_posts[i['id']] = i['link']

    print(post['id'], sorted(distances[post['id']].items(), key=operator.itemgetter(1)))
    for j, i in enumerate(sorted(distances[post['id']].items(), key=operator.itemgetter(1))[0:3]):
        txt += '"' + str(j) + '": "' + i[0] + '", '
        #txt += '"' + str(j) + '": ["' + i[0] + '", "' + dict_posts[i[0]] + '"], '
    txt = txt[0:-2] + '}'
    return txt

blog = sys.argv[1]
posts = parse(blog)

print("filtering post")

for i, post in enumerate(posts):
    posts[i]['filtered']    = filtertxt(post['content'])
    posts[i]['frequency']   = frequency(posts[i]['filtered'])
    posts[i]['digest']      = md5(post['content']).hexdigest()

print ("distances")

distances = {}
for i in posts:
    distances[i['id']] = {}

posts_len = len(posts)

for i in xrange(posts_len):
    post_i = posts[i]
    for j in xrange(i+1, posts_len):
        post_j = posts[j]
        if post_i['id'] != post_j['id'] and post_i['digest'] != post_j['digest']:
            dist = cosDist(post_i['frequency'], post_j['frequency'])
            distances[post_i['id']][post_j['id']] = dist
            distances[post_j['id']][post_i['id']] = dist


print("save to db")

for i in posts:
    try:
        res = Reccommend.get((Reccommend.blog == blog) & (Reccommend.post_id == i['id']))
        #update
        res.posts = sort_distances(posts, distances, i)
        res.digest = i['digest']
        res.save()
    except: #save
        Reccommend.create(blog=blog, post_id=i['id'], title=i['title'], link=i['link'], digest=i['digest'], posts=sort_distances(posts, distances, i))

print('sucessful write')




'''
create table if not exists reccommend (id int(11) not null auto_increment, blog varchar(255), post_id varchar(45), title varchar(255), link varchar(255), posts text default null, primary key (id)) engine=InnoDB
'''