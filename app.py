#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import PickleType
from sqlalchemy import CheckConstraint, func
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from datetime import datetime, timedelta
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    genres = db.Column(PickleType) # https://stackoverflow.com/questions/14692350/how-can-i-insert-arrays-into-columns-on-a-database-table-for-my-pyramid-app
    address = db.Column(db.String(120), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column (db.String(), default = '')
    shows = db.relationship('Show', backref = 'Venue', lazy = True, cascade="all, delete-orphan")


#artist1 = Artist(name = 'Myself', genres = ['Pop', 'Funk', 'Jazz'], city = 'Al-Ola', state = 'Jizan', phone = '1313131313', website = 'www.google.com', image_link = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fprestigiousstarawards.com%2Fwp-content%2Fuploads%2F2019%2F11%2FAwards-Ceremony-Venue-One-Moorgate-Place-Prestigious-Venues.jpg&imgrefurl=https%3A%2F%2Fprestigiousstarawards.com%2Fvenue%2Fone-moorgate-place&tbnid=H_rs16FUG_xIhM&vet=12ahUKEwiAntWIsbPwAhVQ0YUKHWAmDnwQMygBegUIARDAAQ..i&docid=yVgqjKycMcd_jM&w=1200&h=600&q=venue%20place&safe=strict&ved=2ahUKEwiAntWIsbPwAhVQ0YUKHWAmDnwQMygBegUIARDAAQ')


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    genres = db.Column(PickleType) 
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = True)
    seeking_description = db.Column (db.String(), default = '')
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref = 'Artist', lazy = True)

#Show is like a connector between an artist and a venue at a specific time
#Many venues can have many artists, under the conidition that they are working in different times
# Assuming a 6-hour booking per show (shows as an upcoming show)
class Show(db.Model):
  __tablename__ = "Show"
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
  start_time = db.Column(db.String(120), nullable = False)

show_time = 6

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.order_by('state').order_by('city').all()
  print('venues are')
  print(venues)
  cities = []
  #Append initial venue into cities, to avoid issues with for loop, and to avoid redundant if statements in loop
  cities.append({
    'city': venues[0].city,
    'state' : venues[0].state,
    'venues' : [{
    'id' : venues[0].id, 
    'name' : venues[0].name,
    'num_upcoming_shows' : venue_upcoming_shows(venues[0].id)
    }]
  })
  #temporary solution, curr city and curr state, then add if the cobination changed
  
  #Skip first entry as we just entered it when defining cities
  for venue in venues[1:]:
    added = False
    for city in cities:
      if(venue.city == city['city'] and venue.state == city['state']):
        city['venues'].append({
        'id' : venue.id, 
        'name' : venue.name,
        'num_upcoming_shows' : venue_upcoming_shows(venue.id)
        })
        added = True
        break
    if(not added):
      cities.append({
        'city': venue.city,
        'state' : venue.state,
        'venues' : [{
        'id' : venue.id, 
        'name' : venue.name,
        'num_upcoming_shows' : venue_upcoming_shows(venue.id)
        }]
      })
  
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  #print(type(data))
  return render_template('pages/venues.html', areas=cities);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues = Venue.query.filter(func.lower(Venue.name).contains(func.lower(request.form.get('search_term')))).all()
  response={
    "count": len(venues),
    "data": venues
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter_by(id = venue_id).first()
  venue.upcoming_shows = venue_upcoming_shows(venue.id)
  venue.past_shows = venue_past_shows(venue.id)

  return render_template('pages/show_venue.html', venue=venue)
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = True
  try:

    if(request.form.get('seeking_talent') == 'y'): ##HELP, I was not sure how else to do this statement... this seems like its a stupid way of doing it, is there a better way?
      seeking_talent = True
    else:
      seeking_talent = False

    venue = Venue(
      name = request.form.get('name'),
      genres = request.form.getlist('genres'), 
      address = request.form.get('address'), 
      city = request.form.get('city'), 
      state = request.form.get('state'), 
      phone = request.form.get('phone'), 
      website = request.form.get('website_link'),
      facebook_link = request.form.get('facebook_link'),
      seeking_talent = seeking_talent,
      seeking_description = request.form.get('seeking_description'),
      image_link = request.form.get('image_link'))
    db.session.add(venue)
    db.session.commit()
    print('add successful')
    error = False
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('There was an error in adding Venue ' + request.form['name'] + ' :<')

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = True
  venue = Venue.query.get(venue_id)
  name = 'not found'
  print(venue)
  try:
    name = venue.name
    db.session.delete(venue)
    db.session.commit()
    error = False
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  print(Venue)
  print(Artist)
  venues = Venue.query.filter(func.lower(Venue.name).contains(func.lower(request.form.get('search_term')))).all()
  artists = Artist.query.all()
  json_artists = []
  for artist in artists:
    json_artists.append({
      'id' : artist.id,
      'name' : artist.name
    })

  return render_template('pages/artists.html', artists=json_artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artists = Artist.query.filter(func.lower(Artist.name).contains(func.lower(request.form.get('search_term')))).all()
  response={
    "count": len(artists),
    "data": artists
  }
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(id = artist_id).first()

  artist.upcoming_shows = artist_upcoming_shows(artist_id)
  artist.upcoming_shows_count = len(artist.upcoming_shows)

  artist.past_shows = artist_past_shows(artist_id)
  artist.past_shows_count = len(artist.past_shows)

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id = artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.filter_by(id = artist_id).first()
  error = True

  try:
    #print(request.form.get('seeking_venue'))
    artist.name = request.form.get('name')

    artist.genres = request.form.getlist('genres')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.website = request.form.get('website_link')
    artist.facebook_link = request.form.get('facebook_link')

    if(request.form.get('seeking_venue') == 'y'): ##HELP, I was not sure how else to do this statement... this seems like its a stupid way of doing it, is there a better way?
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False

    artist.seeking_description = request.form.get('seeking_description')
    artist.image_link = request.form.get('image_link')
    db.session.commit()
    print('sucess')
    error = False
  except:
    db.session.rollback()
    print('failed')
    error = True 
  finally: 
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id = venue_id).first()
  
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.filter_by(id = venue_id).first()
  error = True
  try:
    
    venue.name = request.form.get('name')
    venue.genres = request.form.getlist('genres')
    venue.address = request.form.get('address')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.website = request.form.get('website_link')
    venue.facebook_link = request.form.get('facebook_link')
    
    if(request.form.get('seeking_talent') == 'y' ): ##HELP, I was not sure how else to do this statement... this seems like its a stupid way of doing it, is there a better way?
      venue.seeking_talent = True
    else:
      print(request.form.get('seeking_venue'))
      venue.seeking_talent = False
    venue.seeking_description = request.form.get('seeking_description')
    venue.image_link = request.form.get('image_link')
    db.session.commit()
    print('sucess')
    error = False
  except:
    db.session.rollback()
    print('failed')
    error = True 
  finally: 
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = True
  try:
    if(request.form.get('seeking_venue') == 'y'): ##HELP, I was not sure how else to do this statement... this seems like its a stupid way of doing it, is there a better way?
      seeking_venue = True
    else:
      seeking_venue = False

    
    artist = Artist(
      name = request.form.get('name'),
      genres = request.form.getlist('genres'), 
      city = request.form.get('city'), 
      state = request.form.get('state'), 
      phone = request.form.get('phone'), 
      website = request.form.get('website_link'),
      facebook_link = request.form.get('facebook_link'),
      seeking_venue = seeking_venue,
      seeking_description = request.form.get('seeking_description'),
      image_link = request.form.get('image_link'))

    db.session.add(artist)
    db.session.commit()

    error = False
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('There was an error in adding Artist ' + request.form['name'] + ' :<')

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  db_shows = Show.query.all()
  if len(db_shows) > 0:
    show = db_shows[0]

    shows = [{
    "venue_id": show.Venue.id,
    "venue_name": show.Venue.name,
    "artist_id": show.Artist.id,
    "artist_name": show.Artist.name,
    "artist_image_link": show.Artist.image_link,
    "start_time": show.start_time
    }]
    
    for show in db_shows[1:]:
      shows.append({
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "artist_id":show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": show.start_time
      })

  else:
    shows = []
  
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = True
  try:

    show = Show(
      artist_id = request.form.get('artist_id'),
      venue_id = request.form.get('venue_id'),
      start_time = request.form.get('start_time'))

    db.session.add(show)
    db.session.commit()
    print('adding successful')
    error = False
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('There was an error in adding your show :<')
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#decrementing show_time as a show window and returns string containing 
def time_now():
  now = datetime.now() + timedelta(hours=-show_time)
  dt_string = now.strftime("%Y-%m-%d %H:%M:%2S")
  return dt_string


def venue_upcoming_shows(venue_id):

  shows = Show.query.filter_by(venue_id = venue_id).all()

  upcoming_shows = []
  now = time_now()

  for show in shows:
    if(show.start_time > now):
      formatted_show = venue_show_format(show)
      upcoming_shows.append(formatted_show)

  return upcoming_shows

def venue_past_shows(venue_id):
  shows = Show.query.filter_by(venue_id = venue_id).all()

  past_shows = []
  now = time_now()

  for show in shows:
    if(show.start_time <= now):
      formatted_show = venue_show_format(show)
      past_shows.append(formatted_show)
  return past_shows

def artist_upcoming_shows(artist_id):
  shows = Show.query.filter_by(artist_id = artist_id).all()

  now = time_now()
  upcoming_shows = []

  for show in shows:
    if(show.start_time > now):
      formatted_show = artist_show_format(show)
      upcoming_shows.append(formatted_show)
  return upcoming_shows

def artist_past_shows(artist_id):
  shows = Show.query.filter_by(artist_id = artist_id).all()
  past_shows = []

  now = time_now()

  for show in shows:
    if(show.start_time <= now):
      formatted_show = artist_show_format(show)
      past_shows.append(formatted_show)
  return past_shows

def artist_show_format(show):
  formatted_show = {
    'venue_id' : show.Venue.id,
    'venue_name' : show.Venue.name,
    'venue_image_link' : show.Venue.image_link,
    'start_time' : show.start_time
    }
  return formatted_show

def venue_show_format(show):
  formatted_show =  {
    'artist_id' : show.Artist.id,
    'artist_name' : show.Artist.name,
    'artist_image_link' : show.Artist.image_link,
    'start_time' : show.start_time
    }
    
  return formatted_show
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

#2021-05-08 04:17:39

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
