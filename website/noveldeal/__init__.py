'''
Created on Sep 10, 2015

@author: xuyan_000
'''

#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask_restful import reqparse, abort, Api, Resource
from account import Account
import logging
import encrypt

#from bson.objectid import ObjectId

# configuration
#DATABASE = 'd:/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#file_handler = logging.FileHandler('/home/ubuntu/weblog')
#file_handler.setLevel(logging.WARNING)
#app.logger.addHandler(file_handler)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("brand")
parser.add_argument("id")
parser.add_argument("category")
#parser.add_argument("index")


#account = Account()
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def connect_db():
#    return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()

@app.before_request
def before_request():
	g.account = Account()
    #g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
    #db = getattr(g, 'db', None)
    #if db is not None:
    #    db.close()

@app.route('/')
def show_entries():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #return render_template('index.html', entries=entries)
	return render_template('index.html')

#@app.route('/add', methods=['POST'])
#def add_entry():
#    if not session.get('logged_in'):
#        abort(401)
#    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
#    g.db.commit()
#    flash('New entry was successfully posted')
#    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error_login = None
	error_register = None
	if request.method == 'POST':
		if 'login-submit' in request.form:
			error_register = None
			#passwd = encrypt.encrypt_password(request.form['password'])
			res = g.account.get_user_account(request.form['email'])
			if res != None:
				app.logger.info('res: %s', res)
				if encrypt.validate_password(res[2], request.form['password']):
					session['logged_in'] = True
					#app.logger.info('res: %s', res)
					session['id'] = str(res[0])
					session['user_name'] = str(res[1])
					flash('You were logged in')
					return redirect(url_for('user'))
				else:
					error_login = 'Invalid password'
			else:
				#exist = g.account.user_exist(request.form['email'])
				#if not exist:
				#	error_login = 'Invalid user email'
				#else:
				error_login = 'Invalid user'	
		elif 'register-submit' in request.form:
			error_login = None
			if request.form['password'] != request.form['confirm-password']:
				error_register = 'Different password'
			elif g.account.user_exist(request.form['email']):
				error_register = 'Email has been registered'
			else:
				app.logger.info('request passwd: %s', request.form['password'])
				passwd = encrypt.encrypt_password(request.form['password'])
				app.logger.info('passwd: %s', passwd)
				g.account.insert_user_account(request.form['username'], passwd, request.form['email'])
				_id, _name, _passwd = g.account.get_user_account(request.form['email'])
				session['logged_in'] = True
				session['id'] = str(_id)
				session['user_name'] = str(_name)
				flash('You were logged in')
				return redirect(url_for('user'))
	return render_template('login.html', error_login=error_login, error_register=error_register)

@app.route('/user', methods=['GET', 'POST'])
def user():
	if not session.get('logged_in'):
		abort(401)
	return render_template('user.html', user=session['user_name'])
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#index = 0	
index = 0	
dict = {}
	
class Brand(Resource):
	def post(self):
		args = parser.parse_args()
		app.logger.info('args: %s', args)
		#id = args['id']
		#brand = args['brand']
		#global index 	
		#global dict
		#if not id:
		#	index += 1
		#	dict[index] = brand
		#else:
		#	dict[id] = brand
		#app.logger.info('interests: %s', dict.values())
		#g.account.update_user_interest(ObjectId(session['id']), dict.values())
		g.account.update_product(args['brand'], args['category'], args['id'])
		#brands = g.account.get_user_interest(ObjectId(session['id']))
		#dict[index] = brand
		#index = args['index']
        #args = parser.parse_args()
        #task = {'task': args['task']}
        #TODOS[todo_id] = task
        #return task, 201	
		#app.logger.info('brand: %s', brand)
		
		#print brand
		#return {"brand":brand, 'id':index}
		return {}
		
	#def get(self):
	#	args = parser.parse_args()
        #index = args['index']
		#abort_if_todo_doesnt_exist(todo_id)
        #return TODOS[todo_id]
		#app.logger.info('brand: %s', brand)
	#	app.logger.info('args: %s', args)
		#print brand
	#	return []

	def delete(self):
		args = parser.parse_args()
		#index = args['index']
        #abort_if_todo_doesnt_exist(todo_id)
        #del TODOS[todo_id]
        #return '', 204
		#app.logger.info('brand: %s', brand)
		app.logger.info('args: %s', args)
		#print brand
		#id = args['id']
		#global index 	
		#global dict
		#dict.pop(int(id), None)
			#dict[id] = brand
		#app.logger.info('interests: %s', dict.values())
		g.account.delete_product(args['brand'], args['category'], session['id'])
		#g.account.update_user_interest(ObjectId(session['id']), dict.values())
		return {}
		
	def put(self):
		args = parser.parse_args()
        #args = parser.parse_args()
        #task = {'task': args['task']}
        #TODOS[todo_id] = task
        #return task, 201	
		#app.logger.info('brand: %s', brand)
		app.logger.info('args: %s', args)
		#print brand
		#id = args['id']
		#global index 	
		#global dict
		#brand = args['brand']
		#if not id:
		#	index += 1
		#	dict[index] = brand
		#else:
		#	dict[id] = brand
		
		#app.logger.info('interests: %s', dict.values())
		g.account.insert_product(args['brand'], args['category'], session['id'])
		return {}
		#return {"brand":brand, 'id':index}
		
	
	
class BrandList(Resource):
    def get(self):
		products = g.account.get_user_interest(session['id'])
		res = []
		#global index 	
		#global dict
		#index = 0
		#dict = {}
		#index = 1
		for product in products:
			res.append({'id':product[0], "brand":product[1], 'category':product[2]})
			#dict[index] = brand
			#index += 1
		app.logger.info('res: %s', res)
		return res
	
api.add_resource(BrandList, '/account')
api.add_resource(Brand, '/account/update/')	
if __name__ == '__main__':
    #init_db()
	app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=80, debug=True)
