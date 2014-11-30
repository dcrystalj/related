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
import networkx as nx
import matplotlib.pyplot as plt
from pylab import *

reload(sys)
sys.setdefaultencoding('utf-8')

def frequency_tuple(string):
    """
    return dict of frequncy for each quadruple of letters
    """
    #4
    #string = ["%s%s%s%s" %(string[i],string[i+1],string[i+2],string[i+3]) for i in range(len(string)-4)]
    #5
    string = ["%s%s%s%s%s" %(string[i],string[i+1],string[i+2],string[i+3],string[i+4]) for i in range(len(string)-5)]
    return Counter(string)

def frequency_words(string):
    """
    return dict of frequncy for each word
    """
    return Counter(string.split())


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


blog = sys.argv[1]
blog_name = sys.argv[2]
posts = parse(blog)

print("filtering post")

for i, post in enumerate(posts):
    filtered                    = filtertxt(post['content'])
    posts[i]['tuple_frequency'] = frequency_tuple(filtered)
    posts[i]['word_frequency']  = frequency_words(filtered)

print ("calculating distances")

tuple_distances = {}
word_distances = {}
for i in posts:
    tuple_distances[i['id']] = {}
    word_distances[i['id']] = {}

posts_len = len(posts)

for i in xrange(posts_len):
    p_i = posts[i]
    print(i),
    for j in xrange(i+1, posts_len):
        p_j = posts[j]
        #if p_i['id'] != p_j['id'] and p_i['title'] != p_j['title']:
        tuple_dist = cosDist(p_i['tuple_frequency'], p_j['tuple_frequency'])
        tuple_distances[p_i['id']][p_j['id']] = tuple_dist
        tuple_distances[p_j['id']][p_i['id']] = tuple_dist

        word_dist = cosDist(p_i['word_frequency'], p_j['word_frequency'])
        word_distances[p_i['id']][p_j['id']] = word_dist
        word_distances[p_j['id']][p_i['id']] = word_dist


#check if directory exists before saving figures
if not os.path.isdir(blog_name): os.makedirs(blog_name)

print("Draw graph")

#different tresholds
for t in range(30, 85, 5):
    treshold = t/100.0
    print('plot'+str(treshold))


    #######TUPLES############
    g = nx.Graph()

    #save edges below treshold in graph
    edges = [(j[0], i) for i in tuple_distances.iterkeys() for j in tuple_distances[i].iteritems() if j[1] < treshold]
    g.add_edges_from(edges)


    #save graph in image
    plt.figure()
    nx.draw(g, with_labels=False)
    title(str(treshold))
    plt.savefig(blog_name + "/tuples" + blog_name + "_" + str(treshold*100)+"_.png")
    plt.close()

    #######WORDS############
    g = nx.Graph()

    #save edges below treshold in graph
    edges = [(j[0], i) for i in word_distances.iterkeys() for j in word_distances[i].iteritems() if j[1] < treshold]
    g.add_edges_from(edges)


    #save graph in image
    plt.figure()
    nx.draw(g, with_labels=False)
    title(str(treshold))
    plt.savefig(blog_name + "/words" + blog_name + "_" + str(treshold*100)+"_.png")
    plt.close()




'''TODO compare methods difference'''
# for i in tuple_distances.iterkeys():
#     for j in tuple_distances[i].iteritems():
#         if j[1] < treshold:
#             g.add_edge(j[0], i)


'''

tuple_d = {}
for i in tuple_distances.iterkeys():
    tuple_d[i] = [j[0] for j in tuple_distances[i].iteritems() if j[1] < treshold]

word_d = {}
for i in word_distances.iterkeys():
    word_d[i] = [j[0] for j in word_distances[i].iteritems() if j[1] < treshold]

def diff(a, b):
    d = 0
    for i in a.iterkeys():
        if i in b:
            if len(a[i]) < len(b[i]):
                [item for item in temp1 if item not in temp2]

'''