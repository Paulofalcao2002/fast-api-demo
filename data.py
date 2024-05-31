from datetime import date as date_type

data = {
    "movies": [
        {"movie_id": 1, "name": "Titanic", "date": date_type(1998, 1, 12)},
        {
            "movie_id": 2,
            "name": "Avengers Infinity War",
            "date": date_type(2018, 4, 26),
        },
        {"movie_id": 3, "name": "Mean Girls", "date": date_type(2004, 7, 9)},
    ],
    "ratings": [
        {
            "rating_id": 1,
            "movie_id": 1,
            "value": 4.5,
            "description": "That was a really nice movie!",
        },
        {
            "rating_id": 2,
            "movie_id": 1,
            "value": 5,
            "description": "The best experience of my life",
        },
    ],
}
