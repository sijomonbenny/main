from flask import Flask,render_template,request,redirect,url_for,flash,session
import database as db
import demjson
import urllib
import numpy
import sklearn
from core import *

app=Flask(__name__)
app.secret_key = "sdfghjkl"

def get_data_from(url):
	data = urllib.request.urlopen(url)

	return demjson.decode(data.read())


@app.route('/',methods=['get','post'])
def home():
	return render_template('user_app/index.html')

@app.route('/forgot',methods=['get','post'])
def forgot():

	return render_template('user_app/forgot.html')

@app.route('/forgot_submit/',methods=['post'])
def forgot_submit():
	data={}
	if 'login' in request.form:
		name=request.form['username']
		mob=request.form['mob']
		newpas=request.form['password']
		print(name)
		q="select u.username,c.phone from user_login u,users c where username='%s' and phone='%s'"%(name,mob)
		res=db.select(q)
		print(res)
		if(len(res)==1):
			q="update user_login set password='%s' where username='%s'"%(newpas,name)
			res=db.update(q)
			print(res)
			data['status'] = 'success'
			data['data'] = res
		else:
			data['status'] = 'Failed'
		print(data)

	return demjson.encode(data)

	
# @app.route('/',methods=['get','post'])
# def home():
#   return render_template('user_app/public_home.html')

@app.route('/register',methods=['get','post'])
def register():
	return render_template('user_app/register.html')

@app.route('/login_action/',methods=['get','post'])
def login_action():
	data = {}
	if 'login' in request.form:
		name=request.form['username']
		pas=request.form['password']
		features=request.form['features']
		s="select * from user_login where username='%s' and password='%s'"%(name,pas)
		sel=db.select(s)
		if len(sel)>0:
			bool = get_login_id(features)
			print(bool)
			if bool != -1: 
				session['login_id'] = sel[0]['login_id']
				data['status'] = 'success'
				data['data'] = sel
			else:
				data['status'] = 'failed'
				data['reason'] = 'Time difference'
		else:
			data['status'] = 'failed'
			data['reason'] = 'Username or password is incorrect'
	return demjson.encode(data)

@app.route('/register_action/',methods=['get','post'])
def register_action():
	data={}
	if 'register' in request.form:
		fnam=request.form['fname']
		lnam=request.form['lname']
		ag=request.form['age']
		d=request.form['dob']
		plac=request.form['place']
		ci=request.form['city']
		st=request.form['state']
		eml=request.form['email']
		phn=request.form['phone']
		user=request.form['user']
		passw=request.form['pass']
		features=request.form['features']
		s="select username,password from user_login where username='%s'"%(user)
		sel=db.select(s)
		
		if(len(sel)==1):
			data['status'] = 'Username Already Exists'
		else:
			lo="insert into user_login(username,password,features,login_type)values('%s','%s','%s','user')"%(user,passw,features)
			log=db.insert(lo)
			print(log)
			q="insert into users(login_id,f_name,l_name,age,dob,place,city,state,email,phone_no)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(log,fnam,lnam,ag,d,plac,ci,st,eml,phn)
			res=db.insert(q)
			data['status'] = 'Successfully Registered'
			data['data'] = sel
			train()
				 	
	return demjson.encode(data)



@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('home'))


@app.route('/user_home',methods=['get','post'])
def user_home():

	mid=[]

	login_id = session['login_id']
	q = db.select("select f_name from users where login_id = '%s' " %(login_id))[0]['f_name']
	q1 = db.select("select email from users where login_id = '%s' " %(login_id))[0]['email']
	res= db.select("select * from mail where t_id=(select email from users where login_id='%s')" % login_id)


	return render_template('user_app/mailbox.html',emails = res,data=q)


@app.route('/sentmail',methods=['get','post'])
def sentmail():
	
	login_id = session['login_id']
	q = db.select("select f_name from users where login_id = '%s' " %(login_id))[0]['f_name']
	q1 = db.select("select email from users where login_id = '%s' " %(login_id))[0]['email']
	res= db.select("select * from mail where f_id=(select email from users where login_id='%s')" % login_id)

	return render_template('user_app/sentmail.html',emails=res,data=q)  



@app.route('/readmail',methods=['get','post'])
def readm():
	mail_id  = request.args['mail_id']
	q = "select * from mail where mail_id='%s'" % mail_id
	res = db.select(q)
	return render_template('user_app/read-mail.html',data=res)  
	


@app.route('/compose',methods=['get','post'])
def compose():
	login_id = session['login_id']
	q = db.select("select f_name from users where login_id = '%s' " %(login_id))[0]['f_name']
	print(q)
	return render_template('user_app/compose.html',data=q)


@app.route('/compose_action',methods=['get','post'])
def cmp():
	login_id = session['login_id']
	q = db.select("select f_name from users where login_id = '%s' " %(login_id))[0]['f_name']
	q1 = db.select("select email from users where login_id = '%s' " %(login_id))[0]['email']

	if 'submit' in request.form:
		t_id=request.form['t_id']
		sub=request.form['sub']
		msg= request.form['msg']
		# lo="insert into mail_id(t_id,f_id,sub,msg)values('%s','%s','%s')"%(user,passw,features)
		q2="insert into mail(t_id,f_id,sub,msg)values('%s','%s','%s','%s')"%(t_id,q1,sub,msg)
		res=db.insert(q2)
		return redirect(url_for('user_home'))


app.run(debug=True,port=5001)

