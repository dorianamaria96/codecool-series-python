from data import data_manager
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows_paginated(page_number):
    return data_manager.execute_select("""
        SELECT shows.id as id,
            shows.title as title,
            shows.year as release_year,
            shows.runtime as average_runtime_length,
            round(CAST(shows.rating AS NUMERIC), 1) as rating,
            string_agg(genres.name, ', '  ORDER BY genres.name) as genres,
            shows.trailer as trailer,
            shows.homepage as homepage
        FROM shows
        JOIN show_genres sg on shows.id = sg.show_id
        JOIN genres ON sg.genre_id = genres.id
        GROUP BY shows.id, title
        ORDER BY rating DESC, title
        LIMIT 15
        OFFSET ((%(page_number)s)- 1) * 15;
        """, {'page_number': page_number})


def get_show(show_id):
    return data_manager.execute_select("""
    SELECT shows.id as id,
            shows.title as title,
            shows.year as release_year,
            shows.runtime as runtime,
            round(CAST(shows.rating AS NUMERIC), 1) as rating,
            string_agg(genres.name, ', '  ORDER BY genres.name) as genres,
            shows.trailer as trailer,
            shows.overview
        FROM shows
        JOIN show_genres sg on shows.id = sg.show_id
        JOIN genres ON sg.genre_id = genres.id
        WHERE show_id = %(show_id)s
        GROUP BY shows.id, title; 
    """, {'show_id': show_id})


def get_actors_for_show(show_id):
    return data_manager.execute_select("""
    SELECT actors.name
    FROM actors
    JOIN show_characters sc on actors.id = sc.actor_id
    JOIN shows s on sc.show_id = s.id
    WHERE s.id = %(show_id)s
    LIMIT 3;
    """, {'show_id': show_id})


def get_seasons(show_id):
    return data_manager.execute_select("""
    SELECT seasons.*
    FROM seasons
    JOIN shows on seasons.show_id = shows.id
    WHERE shows.id = %(show_id)s
    GROUP BY seasons.id
    """, {'show_id': show_id})


def get_actors():
    return data_manager.execute_select("""
    SELECT split_part(actors.name,' ',1) as first_name,
       actors.id,
        array_agg(s.title) as shows
    FROM actors
    JOIN show_characters sc on actors.id = sc.actor_id
    JOIN shows s on s.id = sc.show_id
    GROUP BY actors.id, actors.birthday
    ORDER BY  actors.birthday
    LIMIT 100;""")


def get_average_rating():
    return data_manager.execute_select("""
    SELECT ROUND((AVG(rating)),2) as rating_average
    FROM shows
    """)[0]['rating_average']


def get_shows_by_rating():
    return data_manager.execute_select("""
    SELECT shows.id, shows.title AS title, TRUNC((AVG(shows.rating)),2) AS rating,
        COUNT(sc.id) as actors_count
    FROM shows
    JOIN show_characters sc on shows.id = sc.show_id
    GROUP BY shows.id
    ORDER BY actors_count DESC
    LIMIT 10;""")


def get_ordered_shows(order):
    return data_manager.execute_select("""
    SELECT shows.title as title,
       ROUND(shows.rating) as rating,
       COUNT(e.episode_number) as episode_count
    FROM shows
    JOIN seasons s on shows.id = s.show_id
    JOIN episodes e on s.id = e.season_id
    GROUP BY shows.title, shows.rating
    ORDER BY 
     CASE WHEN %(order)s = 'ASC' THEN COUNT(e.episode_number) END,
     CASE WHEN %(order)s = 'DESC' THEN COUNT(e.episode_number) END DESC, shows.title
    LIMIT 10""", {'order': order})


def get_actors_birthday():
    return data_manager.execute_select("""
    SELECT name, EXTRACT(DAY FROM birthday) as day_of_birth FROM actors
    WHERE death IS NULL
    ORDER BY birthday
    LIMIT 100""")


def get_genres():
    return data_manager.execute_select("""
    SELECT * FROM genres""")


def get_actors_by_search(genre_id, search):
    return data_manager.execute_select("""
    SELECT actors.name as actor,
       sg.genre_id as genre_id
    FROM actors
    JOIN show_characters ON show_characters.actor_id = actors.id
    JOIN show_genres sg on show_characters.show_id = sg.show_id
    WHERE genre_id = %(genre_id)s AND upper(actors.name) LIKE %(search)s
    LIMIT 20
    """, {'genre_id': genre_id, 'search': f"%{search}%"})


def get_actors_by_genre(genre_id):
    return data_manager.execute_select("""
    SELECT actors.name as actor,
       show_genres.genre_id as genre
    FROM actors
    JOIN show_characters on actors.id = show_characters.actor_id
    JOIN show_genres on show_characters.show_id = show_genres.show_id
    WHERE show_genres.genre_id = %(genre_id)s
    GROUP BY genre, actor
    LIMIT 20;""", {'genre_id': genre_id})


def shows_with_more_than_5_related_genres():
    return data_manager.execute_select("""
    SELECT shows.title AS title
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY title, year
    HAVING COUNT(genres.name) > 5
    ORDER BY shows.year ASC""")


def selected_show(show_title):
    return data_manager.execute_select("""
    SELECT EXTRACT(YEAR FROM shows.year) as production_year,
       EXTRACT(YEAR FROM shows.year) + 25 as anniversary,
       COUNT(seasons.show_id) as number_of_seasons,
       ROUND(shows.rating) as rating
    FROM shows
    JOIN seasons on seasons.show_id = shows.id
    WHERE shows.title = %(show_title)s
    GROUP BY shows.id
    """, {'show_title': show_title})


def get_hundred_actors():
    return data_manager.execute_select("""
    SELECT id,
           split_part(actors.name, ' ', 1) AS name,
           birthday
    FROM actors
    ORDER BY birthday
    LIMIT 100;
    """)


def get_actors_work(actors_id):
    return data_manager.execute_select("""
    SELECT actors.id,
           shows.title
    FROM actors
    JOIN show_characters ON actors.id=show_characters.actor_id
    JOIN shows ON show_characters.show_id=shows.id
    WHERE actors.id = %(actors_id)s;
    """, {'actors_id': actors_id})
