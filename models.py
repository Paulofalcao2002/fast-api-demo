from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    date = Column(DateTime(), index=True)

    ratings = relationship("Rating", back_populates="movie")


class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, index=True)
    description = Column(String(300), index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))

    movie = relationship("Movie", back_populates="ratings")
