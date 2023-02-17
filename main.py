from flask import Flask, render_template, jsonify, url_for, request
from data import queries
import math
from dotenv import load_dotenv
from decimal import *

load_dotenv()
app = Flask('codecool_series')
SHOWS_PER_PAGE = 15


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=False)


@app.route('/shows/', methods=['GET'])
@app.route('/shows/most-rated/', methods=['GET'])
def most_rated_shows(shows_per_page=SHOWS_PER_PAGE):
    total_shows = queries.get_shows()
    rated_shows = queries.get_most_rated_shows_paginated(1)
    page_number = request.args.get('page_number', '')
    total_number_shows = len(total_shows)
    pages_number = math.ceil(total_number_shows / shows_per_page)
    if page_number:
        rated_shows = queries.get_most_rated_shows_paginated(page_number)
    return render_template('most_rated_shows.html', most_rated_shows=rated_shows, pages_number=pages_number)


@app.route('/show/<show_id>')
def show_detailed_view(show_id):
    show_details = queries.get_show(show_id)
    actors = queries.get_actors_for_show(show_id)
    if show_details[0]['trailer'] is not None:
        video_id = show_details[0]['trailer'][-11::]
    seasons = queries.get_seasons(show_id)
    return render_template('show_detailed_view.html', show_details=show_details, actors=actors, video_id=video_id, seasons=seasons)


@app.route('/actors')
def get_actors():
    actors = queries.get_actors()
    return render_template('actors.html', actors=actors)


@app.route('/ratings')
def get_rating():
    average_rating = queries.get_average_rating()
    shows_rating = queries.get_shows_by_rating()
    print(average_rating)
    return render_template('ratings.html', shows_rating=shows_rating, average_rating=average_rating)


@app.route('/api/ordered-shows')
def ordered_shows_json():
    order = request.args.get('sortState')
    return jsonify(queries.get_ordered_shows(order=order))


@app.route('/ordered-shows', methods=['GET'])
def ordered_shows():
    return render_template('ordered-shows.html')


@app.route('/birthday-actors')
def birthday_actors():
    actors = queries.get_actors_birthday()
    return render_template('birthday-actors.html', actors=actors)


@app.route('/filter-actors', methods=['GET', 'POST'])
def filter_actors():
    genres = queries.get_genres()
    return render_template('filter_actors.html', genres=genres)


@app.route('/api/search-actor-by-name')
def search_actor_by_name():
    search = request.args.get('searchedActor')
    genre_id = request.args.get('selectedGenre')
    search = search.upper()
    print(search)
    return jsonify(queries.get_actors_by_search(genre_id, search))


@app.route('/api/search-actor-by-genre')
def search_actor_by_genre():
    genre_id = request.args.get('selectedGenre')
    return jsonify(queries.get_actors_by_genre(genre_id))


@app.route('/shows-with-more-than-5-genres')
def shows_with_more_than_5_genres():
    shows = queries.shows_with_more_than_5_related_genres()
    return render_template('shows-with-more-than-5-genres.html', shows=shows)


@app.route('/api/shows-with-more-than-5-genres')
def selected_show_details():
    show_title = request.args.get('selectedShow')
    return jsonify(queries.selected_show(show_title))


@app.route('/actors2')
def actor():
    actors = queries.get_hundred_actors()
    return render_template('actors2.html', actors=actors)


@app.route('/api/actors2')
def api_actor():
    actors_id = request.args.get('actorsWork')
    return jsonify(queries.get_actors_work(actors_id))



if __name__ == '__main__':
    main()
