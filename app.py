# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request,Markup
import requests as req
from json2html import *
# create the application object
app = Flask(__name__)

data={
	'admin':'admin',
}

polled = {
	'admin':False,
}


signed_in=False
user =''
polls=0

votes ={
	'Inception': 0,
	'Predestination': 0,
	'Shutter Island': 0,
	'Interstellar': 0,
}

@app.route('/')
def get_stats():
	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if not signed_in:
		print('not signed_in')
	else:
		print('signed_in')

	return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if signed_in:
		signed_in=False
		user=''
	error = None
	if request.method == 'POST':
		if (request.form['username'] in data.keys() and data[request.form['username']]==request.form['password']):
			signed_in=True
			user = request.form['username']

			return redirect(url_for('main',username=request.form['username']))

		else:
			error = 'Invalid Credentials. Please try again.'
	return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if not signed_in:
		print('not signed_in')
	else:
		print('signed_in')
	error=None
	if request.method =='POST':
		if request.form['username'] in data.keys():
			error = 'User already exists'
		else:
			data[request.form['username']]=request.form['password']
			polled[request.form['username']]=False
			return redirect('/login')

	return render_template('signup.html',error=error)

@app.route('/main')
def main():
	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if not signed_in:
		print('not signed_in')
	else:
		print('signed_in')

	if signed_in:
		username = request.args['username']
		return render_template('main.html',username=username)
	else:
		return Markup("<h1>Please <a href='/'>sign-in<a></h1>")

@app.route('/rate', methods=['GET', 'POST'])
def rate():
	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if not signed_in:
		print('not signed_in')
	else:
		print('signed_in')
	if signed_in:
		if not polled[user]:
			form_struct =""
			i=0
			if request.method =='POST':
				votes[request.form['movie']]+=1
				polls+=1
				polled[user]=True
				return redirect(url_for('end'))		
			else:
				for key in votes.keys():
					form_struct = form_struct + "<input type='radio' id='"+str(i)+"' name='movie' value='"+key+"'><label for='"+key+"'>"+key+"</label><br>"


				return render_template('rate.html',form_struct=Markup(form_struct))
		else:
			return Markup("<h1>Thanks for polling!</h1>")
	else:
		return Markup("<h1>Please <a href='/'>sign-in<a></h1>")


@app.route('/end')
def end():
	global signed_in
	global user
	global polls
	global polled
	global data
	global votes
	if signed_in:
		res = "<p>"
		for key in votes.keys():
			res+=key+"-"+str(votes[key])+"<br>"
		res+="</p>"

		return render_template('end.html',html = Markup(res),part=polls	)
	else:
		return Markup("<h1>Please <a href='/'>sign-in<a></h1>")



if __name__=="__main__":
	app.run(debug=True)
