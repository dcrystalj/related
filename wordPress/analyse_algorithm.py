from __future__ import print_function
import copy
import csv
import re
import math
from random import *
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
from collections import defaultdict
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

tuple_distances = defaultdict(lambda: {})
word_distances = defaultdict(lambda: {})

posts_len = len(posts)

for i in xrange(posts_len):
    p_i = posts[i]
    #print(i),
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
    nx.draw(g, with_labels=True)
    title(str(treshold))
    plt.savefig(blog_name + "/tuples_label" + blog_name + "_" + str(treshold*100)+"_.png")
    plt.close()

    #######WORDS############
    g = nx.Graph()

    #save edges below treshold in graph
    edges = [(j[0], i) for i in word_distances.iterkeys() for j in word_distances[i].iteritems() if j[1] < treshold]
    g.add_edges_from(edges)


    #save graph in image
    plt.figure()
    nx.draw(g, with_labels=True)
    title(str(treshold))
    plt.savefig(blog_name + "/words_label" + blog_name + "_" + str(treshold*100)+"_.png")
    plt.close()


# for i in tuple_distances.iterkeys():
#     for j in tuple_distances[i].iteritems():
#         if j[1] < treshold:
#             g.add_edge(j[0], i)



all_keys = tuple_distances.keys()
tuple_dist = {} #defaultdict(lambda: [])
word_dist = {} #defaultdict(lambda: [])
for j in all_keys:
    tuple_dist[j] = [i[0] for i in sorted(tuple_distances[j].items(), key=operator.itemgetter(1))]
    word_dist[j]  = [i[0] for i in sorted(word_distances[j].items(), key=operator.itemgetter(1))]


def rnd_distances():
    return [choice(all_keys) for i in range(11)]
random_distances = defaultdict(rnd_distances)

def simmilarity(a, b):
    return len([1 for i in a if i in b])

tuple_vs_word = defaultdict(lambda: 0)
tuple_vs_random = defaultdict(lambda: 0)
word_vs_random = defaultdict(lambda: 0)
num_of_keys = len(tuple_dist.keys()) * 1.0

for k in xrange(1, 11):
    for i in all_keys:
        t_d = tuple_dist[i][0:k]
        w_d = word_dist[i][0:k]
        r_d = random_distances[i][0:k]
        #print (str(t_d[0]) + " " + str(r_d))

        #comment uncomment what you need
        tuple_vs_word[k]   += simmilarity(t_d, w_d)
        tuple_vs_random[k] += simmilarity(t_d, r_d)
        word_vs_random[k]  += simmilarity(w_d, r_d)

        # tuple_vs_word[k]   += 1 if simmilarity(t_d, w_d) > 0 else 0
        # tuple_vs_random[k] += 1 if simmilarity(t_d, r_d) > 0 else 0
        # word_vs_random[k]  += 1 if simmilarity(w_d, r_d) > 0 else 0


    #print(tuple_vs_word[k],(tuple_vs_word[k] / (num_of_keys * k)) * 100, int((tuple_vs_word[k] / (num_of_keys * k)) * 100))
    tuple_vs_word[k]   = round((tuple_vs_word[k]   / (num_of_keys * k)) * 100)
    tuple_vs_random[k] = round((tuple_vs_random[k] / (num_of_keys * k)) * 100)
    word_vs_random[k]  = round((word_vs_random[k]  / (num_of_keys * k)) * 100)

    # tuple_vs_word[k]   = round((tuple_vs_word[k]   / (num_of_keys)) * 100)
    # tuple_vs_random[k] = round((tuple_vs_random[k] / (num_of_keys)) * 100)
    # word_vs_random[k]  = round((word_vs_random[k]  / (num_of_keys)) * 100)

tuple_vs_word   = tuple_vs_word.values()
tuple_vs_random = tuple_vs_random.values()
word_vs_random  = word_vs_random.values()

# tuple_vs_word   = tuple_vs_word.values()
# tuple_vs_random = tuple_vs_random.values()
# word_vs_random  = word_vs_random.values()

plt.figure()
plt.plot(tuple_vs_word, 'g', tuple_vs_random, 'r', word_vs_random, 'b')
plt.ylabel('%')
plt.xlabel('related length')
ax = plt.axes()
ax.set_xlim(0, 10)
ax.set_ylim(-1, 100)
title('tuples & words & random')
plt.savefig(blog_name + "/tuples_words_random_precise" + ".png")
plt.close()


#edges = [(j[0], i) for i in tuple_dist.iterkeys() for j in tuple_distances[i].iteritems() if j[1] < treshold]