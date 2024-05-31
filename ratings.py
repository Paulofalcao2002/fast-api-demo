from fastapi import Path, HTTPException, Body, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from schemas import *
from utils import *
from data import data
import crud
from dependencies import *
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/ratings",
    tags=[Tags.ratings],
)


@router.get("/", response_model=list[RatingOut])
async def get_ratings(db: Session = Depends(get_db)):
    return crud.get_ratings(db)


@router.get(
    "/{rating_id}",
    response_model=RatingOut,
    responses={404: {"description": "The rating was not found"}},
)
async def get_ratings_by_id(
    rating_id: Annotated[int, Path(title="The ID of the rating", example=1)],
    db: Session = Depends(get_db),
):

    results = crud.get_rating(db, rating_id)

    if results == None:
        raise HTTPException(status_code=404, detail="Rating not found")

    return results


@router.get(
    "/movies/{movie_id}",
    response_model=list[RatingOut],
    responses={404: {"description": "The movie was not found"}},
)
async def get_ratings_by_movie_id(
    movie_id: Annotated[int, Path(title="The ID of the movie", example=1)],
    db: Session = Depends(get_db),
):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie doesn't exists!")

    return movie.ratings


@router.post(
    "/",
    response_model=RatingOut,
    responses={
        404: {"description": "Not Found"},
        409: {"description": "Error: Conflict"},
    },
)
async def create_rating(
    rating: Annotated[
        BaseRating,
        Body(
            title="JSON Body of the rating",
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "movie_id": 1,
                        "value": 1,
                        "description": "Disgusting!",
                    },
                },
                "no description": {
                    "summary": "A normal example without description",
                    "description": "A normal example without description",
                    "value": {
                        "movie_id": 1,
                        "value": 4,
                    },
                },
                "movie not in data": {
                    "summary": "A movie that doesn't exists",
                    "description": "If a movie doesn't exists in data (the id is not being used), an http error will be raised",
                    "value": {
                        "movie_id": 6,
                        "value": 3,
                        "description": "Mediocre!",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "movie_id": 1,
                        "description": "No opinions at all!",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):

    movie_in_data = crud.get_movie(db, rating.movie_id)
    if movie_in_data is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return crud.create_rating(db, rating)


@router.put(
    "/{rating_id}",
    response_model=RatingOut,
    responses={404: {"description": "Rating not found"}},
)
async def update_rating(
    rating_id: Annotated[int, Path(title="The ID of the rating", example=1)],
    rating: Annotated[
        BaseRating,
        Body(
            title="JSON Body of the rating",
            examples={
                "normal": {
                    "summary": "A normal put example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "movie_id": 1,
                        "value": 2,
                        "description": "Disgusting but not that bad!",
                    },
                },
                "movie not in data": {
                    "summary": "A movie that doesn't exists",
                    "description": "If the movie_id doesn't exists in data, an http error will be raised",
                    "value": {
                        "movie_id": -1,
                        "value": 2,
                        "description": "Okay!",
                    },
                },
                "rating not in data": {
                    "summary": "A rating that doesn't exists",
                    "description": "If the rating doesn't exists in data, an http error will be raised",
                    "value": {
                        "movie_id": 1,
                        "value": 5,
                        "description": "Who would say this is disgusting?",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "movie_id": "I should be a number",
                        "value": 5,
                        "description": "Who would say this is disgusting?",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):

    rating_result = crud.get_rating(db, rating_id)

    if rating_result is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    movie_result = crud.get_movie(db, rating.movie_id)

    if movie_result is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    crud.update_rating(db, rating_id, rating)

    return crud.get_rating(db, rating_id)


@router.delete(
    "/{rating_id}",
    response_model=RatingOut,
    responses={404: {"description": "The rating was not found"}},
)
def delete_rating(
    rating_id: Annotated[
        int,
        Path(title="The ID of the rating", example=1),
    ],
    db: Session = Depends(get_db),
):
    result = crud.get_rating(db, rating_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    crud.delete_rating(db, result)

    return result
