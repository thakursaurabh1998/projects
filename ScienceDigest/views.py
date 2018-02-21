from models import Base, Categories, Articles, User
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask import make_response, flash
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc, asc
import datetime
import requests
import sys
import random
import string
import codecs
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError


sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# connecting database
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Science Digest"


# handler methods with route decorators

# home page handler
@app.route('/')
@app.route('/digest')
def homeHandler():
    categories = session.query(Categories).all()
    articles = session.query(Articles, User).filter(
        Articles.user_id == User.id
        ).order_by(desc(Articles.time)).limit(5).all()
    return render_template(
        'home.html',
        categories=categories,
        articles=articles)


# category wise articles handler
@app.route('/digest/<string:category_name>/articles/')
def categoryItems(category_name):
    category_name = category_name.replace('+', ' ')
    articles = session.query(Articles).\
        filter_by(category_name=category_name).all()
    categories = session.query(Categories).all()
    if 'username' not in login_session:
        return render_template(
            'publicArticles.html',
            articles=articles,
            category_name=category_name,
            categories=categories)
    else:
        return render_template(
            'articles.html',
            articles=articles,
            category_name=category_name,
            categories=categories)


# article adding handler
@app.route('/digest/new/', methods=['GET', 'POST'])
def itemAdd():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    categories = session.query(Categories).all()
    if request.method == 'POST':
        title = request.form['title']
        about = request.form['description']
        category = request.form['category']
        picture = request.form['picture']
        newArticle = Articles(
            title=title,
            about=about,
            category_name=category,
            time=str(datetime.datetime.now()),
            user_id=login_session['user_id'],
            picture=picture)
        session.add(newArticle)
        session.commit()
        flash("Article has been added.")
        return redirect(url_for('homeHandler'))
    if request.method == 'GET':
        return render_template('newArticle.html', categories=categories)


# single article handler
@app.route('/digest/<string:category_name>/<string:articleTitle>/')
def itemDetails(category_name, articleTitle):
    category_name = category_name.replace('+', ' ')
    articleTitle = articleTitle.replace('+', ' ')
    categories = session.query(Categories).all()
    article = session.query(Articles).filter_by(title=articleTitle).one()
    user = session.query(User).filter_by(id=article.user_id).one()
    return render_template(
        'singleArticle.html',
        article=article,
        user=user,
        categories=categories)


# article edit handler
@app.route('/digest/<string:articleTitle>/edit/', methods=['GET', 'POST'])
def itemEdit(articleTitle):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    articleTitle = articleTitle.replace('+', ' ')
    categories = session.query(Categories).all()
    article = session.query(Articles).filter_by(title=articleTitle).one()
    if article.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You \
are not authorized to edit this article. \
Please create your own article in order to edit.');}\
</script><body onload='myFunction()'>"
    else:
        if request.method == 'POST':
            article.title = request.form['title']
            article.about = request.form['description']
            article.category_name = request.form['category']
            article.time = str(datetime.datetime.now())
            article.picture = request.form['picture']
            session.add(article)
            session.commit()
            flash("Article is edited successfully.")
            return redirect(url_for('homeHandler'))
        if request.method == 'GET':
            return render_template(
                'editArticle.html',
                article=article,
                articleTitle=articleTitle,
                categories=categories)


# article delete handler
@app.route('/digest/<string:articleTitle>/delete/', methods=['GET', 'POST'])
def itemDelete(articleTitle):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    articleTitle = articleTitle.replace('+', ' ')
    article = session.query(Articles).filter_by(title=articleTitle).one()
    categories = session.query(Categories).all()
    if article.user_id != login_session['user_id']:
        return "<script>function myFunction() \
{alert('You are not authorized to delete this article.');}\
</script><body onload='myFunction()'>"
        return redirect(url_for('homeHandler'))
    else:
        if request.method == 'POST':
            session.delete(article)
            session.commit()
            flash("Article is deleted successfully.")
            return redirect(url_for('homeHandler'))
        if request.method == 'GET':
            return render_template(
                'deleteArticle.html',
                categories=categories,
                article=article)


# JSON endpoints
# endpoint for categories of the page
@app.route('/digest.json')
def digestJSON():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    else:
        categories = session.query(Categories).all()
        return jsonify(Digest=[i.serialize for i in categories])


# endpoint for all the articles of a single category
@app.route('/<string:category>/articles.json')
def articlesJSON(category):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    else:
        category = category.replace('+', ' ')
        articles = session.query(Articles).\
            filter_by(category_name=category).all()
        categories = session.query(Categories).all()
        return jsonify(category_name=[i.serialize for i in articles])


# endpoint for a single article
@app.route('/digest/<string:category_name>/<string:articleTitle>/article.json')
def singleArticleJSON(category_name, articleTitle):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    else:
        category_name = category_name.replace('+', ' ')
        articleTitle = articleTitle.replace('+', ' ')
        article = session.query(Articles).\
            filter_by(title=articleTitle).one()
        categories = session.query(Categories).all()
        return jsonify(article=[article.serialize])


# LOGIN
@app.route('/login')
def login():
    if 'username' not in login_session:
        state = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    else:
        flash("Already Logged In")
        return redirect(url_for('homeHandler'))


# facebook oauth
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?\
grant_type=fb_exchange_token&client_id=%s&client\
_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.11/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.11/me?access\
_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.11/me/picture?\
access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius\
: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "You have been logged out"


# google id connection
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '''
    <div class="content">
    <div class="row">
        <div class="col-md-12">
            <h1>Welcome '''
    output += login_session['username']
    output += '''
    !!</h1>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <img style = "width: 200px; height: \
200px;border-radius: 100px;-webkit-border-radius: \
100px;-moz-border-radius: 100px;" src="'''
    output += login_session['picture']
    output += '''">
        </div>
    </div>
</div>
    '''
    flash("You are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
# This method is to add a new user to the database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# This method is to get the information of a registered user from the database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# This method returns user_id
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# logging out handler
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        elif login_session['provider'] == 'facebook':
            fbdisconnect()
        del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in.")
    return redirect(url_for('homeHandler'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
