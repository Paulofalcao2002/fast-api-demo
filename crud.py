from sqlalchemy.orm import Session
import models, schemas
from fastapi.encoders import jsonable_encoder


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()


def create_movie(db: Session, movie: schemas.BaseMovie):
    db_movie = models.Movie(name=movie.name, date=movie.date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie: schemas.MovieOut):
    db.delete(movie)
    db.commit()


def update_movie(db: Session, movie_id: int, new_movie: schemas.BaseMovie):
    db.query(models.Movie).filter_by(movie_id=movie_id).update(
        jsonable_encoder(new_movie)
    )
    db.commit()


def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rating).offset(skip).limit(limit).all()


def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.rating_id == rating_id).first()


def get_ratings_by_movie_id(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()


def create_rating(db: Session, rating: schemas.BaseRating):
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def delete_rating(db: Session, rating: schemas.RatingOut):
    db.delete(rating)
    db.commit()


def update_rating(db: Session, rating_id: int, new_rating: schemas.BaseRating):
    db.query(models.Rating).filter_by(rating_id=rating_id).update(
        jsonable_encoder(new_rating)
    )
    db.commit()
