from flask import Flask, render_template, request, redirect, url_for,\
 flash, jsonify
from flask import session as login_session
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import json
import httplib2
import requests
from database_setup import Base, User, Beer, MenuItem
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import inspect

app = Flask(__name__)

# Create session and connect to DB ##
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Sign In with Google
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Beer App"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # req_json = req.decode('utf8').replace("'", '"')
    # result = json.loads(req_json)

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
        print "Token's client ID does not match app's."
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
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h4>Welcome, '
    output += login_session['username']
    output += '!</h4>'
    flash('You are logged in as %s' % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(
        username=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        userid = session.query(User).filter_by(email=email).one().id
        return userid
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']

    return redirect(url_for('showAll'))


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({
                           'message': 'user already exists'}), 200

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(
        {'username': user.username}), 201


@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


# JSON APIs for all items

@app.route('/beer/<int:beer_id>/JSON')
def beerMenuJSON(beer_id):
    beer = session.query(Beer).filter_by(id=beer_id).one()
    items = session.query(MenuItem).filter_by(
        beer_id=beer.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/beer/<int:beer_id>/<int:menu_id>/JSON')
def menuItemJSON(beer_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/beer/JSON')
def beerJSON():
    beers = session.query(Beer).all()
    return jsonify(beers=[r.serialize for r in beers])


# Show a list of all beer styles
@app.route('/')
@app.route('/beer/')
def showAll():
    beers = session.query(Beer).all()
    menu_item = session.query(MenuItem).all()
    return render_template('beers.html', beers=beers,
                           menuItem=MenuItem, login=login_session)


# Show a specific beer menu
@app.route('/beer/<int:beer_id>/')
def showMenu(beer_id):
    inspector = inspect(engine)
    # print inspector.get_table_names()
    # print inspector.get_columns('Beer')
    beer = session.query(Beer).filter_by(id=beer_id).one()
    beerList = session.query(MenuItem).filter_by(beer=beer).all()
    items = session.query(MenuItem).filter_by(beer_id=beer.id).all()
    return render_template('menu.html', beer=beer,
                           items=items, beer_id=beer_id,
                           beerList=beerList, login=login_session)


# Show a menu item
@app.route('/beer/<int:beer_id>/<int:menu_id>/')
def showItem(beer_id, menu_id):
    items = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return render_template('item.html', items=items, login=login_session)


# Add a new menu item
@app.route('/beer/<int:beer_id>/new/', methods=['GET', 'POST'])
def newMenuItem(beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        beer = session.query(Beer).filter_by(name=request.form['beer']).one()
        newItem = MenuItem(
            name=request.form['name'], description=request.form['description'],
            user_id=login_session['user_id'], beer=beer)
        session.add(newItem)
        flash('New item %s Successfully Added- cheers!' % newItem.name)
        session.commit()
        return redirect(url_for('showMenu', beer_id=newItem.beer_id,
                                login=login_session))
    else:
        return render_template('newmenuitem.html', beer_id=beer_id)


# Edit a Beer Menu item
@app.route('/beer/<int:beer_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(beer_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        session.add(editItem)
        session.commit()
        flash('Item Successfully Edited %s' % editItem.name)
        return redirect(url_for('showMenu', beer_id=beer_id,
                                login=login_session))
    else:
        return render_template('editmenuitem.html',
                               beer_id=beer_id, menu_id=menu_id,
                               item=editItem, login=login_session)


# Delete a beer menu item
@app.route('/beer/<int:beer_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(beer_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted %s' % itemToDelete.name)
        return redirect(url_for('showMenu', beer_id=beer_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete,
                               login=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)