#!/usr/bin/env python2.7

import psycopg2


article_views = open('article_views.txt', 'w+')
author_views = open('author_views.txt', 'w+')
errors = open('errors.txt', 'w+')


def connect():
    # connect to database
    return psycopg2.connect("dbname=news")
    # returns a connection to database


def pro1():
    db = connect()
    c = db.cursor()
    c.execute("""select count(*) as cnt,articles.title
        from log,articles where
        log.path='/article/'||articles.slug
        group by articles.title
        order by cnt desc limit 3;""")
    count = c.fetchall()
    for item in count:
        article_views.write('"'+str(item[1])+'"'+' - '+str(item[0])+" views\n")
    db.close()


def pro2():
    db = connect()
    c = db.cursor()
    c.execute("""select count(*) as cnt, authors.name
        from log,articles,authors
        where authors.id = articles.author and
        log.path = '/article/'||articles.slug
        group by authors.name
        order by cnt desc;""")
    count = c.fetchall()
    for item in count:
        author_views.write(str(item[1])+' - '+str(item[0])+" views\n")
    db.close()


def pro3():
    db = connect()
    c = db.cursor()
    c.execute("""create view total as
        select count(*) as total,date(time)
        from log
        group by date(time)
        order by date(time);""")
    c.execute("""create view errors as
        select count(*) as errors,date(time)
        from log
        where status like '4%'
        group by date(time)
        order by date(time);""")
    c.execute("""create view percentage as
        select (cast(errors.errors as float)/cast(total.total as float))*100
        as percentage,total.date
        from errors natural join total;""")
    c.execute("""select * from percentage
        where percentage>1;""")
    count = c.fetchall()
    for item in count:
        errors.write(str(item[1])+' - '+"%.2f" % item[0]+"% errors\n")
    db.close()

pro1()
pro2()
pro3()
