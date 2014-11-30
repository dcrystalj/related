import MySQLdb as mdb
import peewee
from peewee import *

db = MySQLDatabase('wordpress', user='root', passwd='root')

class Reccommend(peewee.Model):
    post_id=peewee.CharField()
    blog =  peewee.CharField()
    title = peewee.CharField()
    link =  peewee.CharField()
    digest = peewee.CharField()
    posts = peewee.TextField()

    class Meta:
        database = db

#db.create_tables([Reccommend])