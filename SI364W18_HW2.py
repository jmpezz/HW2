## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album: ', [Required])
	album_rating = RadioField('How much do you like this album? (1 low, 3 high)', [Required], choices = [('1', '1'), ('2', '2'), ('3', '3')])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform', methods = ['GET'])
def artist_form():
	return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET'])
def artist_info():
	api_access = 'http://itunes.apple.com/search?term=' + request.args.get('artist')
	get_req = requests.get(api_access)
	json_info = json.loads(get_req.text)
	return render_template('artist_info.html', objects = json_info['results'])

@app.route('/artistlinks')
def artist_links():
	return render_template(artist_links)

@app.route('/specific/song/<artist_name>')
def spec_song(artist_name):
	api_access = 'http://itunes.apple.com/search?term=' + artist_name
	get_req1 = requests.get(api_access)
	json_info = json.loads(get_req1.text)
	result = json_info['results']
	return render_template('specific_artist.html', results = result)

@app.route('/album_entry', methods = ['GET'])
def alb_entry():
	if request.method == 'GET':
		alb_form = AlbumEntryForm()
		return render_template('album_entry.html', form = alb_form)

@app.route('/album_result', methods = ['GET'])
def album_result():
	if request.method == 'GET':
		alb_name = request.args.get('album_name')
		alb_rating = request.args.get('album_rating')
		alb_list = (alb_name, alb_rating)
		return render_template('album_data.html', results = alb_list)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
