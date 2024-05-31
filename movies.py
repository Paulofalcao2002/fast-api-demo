from fastapi import Path, HTTPException, Body, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from schemas import *
from data import data
from utils import *
import crud
from dependencies import *
from sqlalchemy.orm import Session

router = APIRouter(prefix="/movies", tags=[Tags.movies])


@router.get("/", response_model=list[MovieOut])
async def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)


@router.get(
    "/{movie_id}",
    response_model=MovieOut,
    responses={404: {"description": "The movie was not found"}},
)
async def get_movie_by_id(
    movie_id: Annotated[
        int,
        Path(title="The ID of the movie", example=1),
    ],
    db: Session = Depends(get_db),
):
    result = crud.get_movie(db, movie_id)

    if result == None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return result


@router.post(
    "/",
    response_model=MovieOut,
)
async def create_movie(
    movie: Annotated[
        BaseMovie,
        Body(
            title="JSON body of the movie",
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "John Wick 4",
                        "date": "2023-03-23",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Titanic",
                        "date": "1998-01",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    return crud.create_movie(db, movie)


@router.put(
    "/{movie_id}",
    response_model=MovieOut,
    responses={404: {"description": "Movie not found"}},
)
async def update_movie(
    movie_id: Annotated[
        int,
        Path(title="The ID of the movie", example=1),
    ],
    movie: Annotated[
        BaseMovie,
        Body(
            title="JSON body of the movie",
            examples={
                "normal": {
                    "summary": "A normal put example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Titanic 3D",
                        "date": "1998-01-12",
                    },
                },
                "movie not in data": {
                    "summary": "A movie that doesn't exists",
                    "description": "If the movie_id doesn't exists in data, an http error will be raised",
                    "value": {
                        "name": "Titanic",
                        "date": "1998-01-12",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Titanic",
                        "date": "1998-01",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    result = crud.get_movie(db, movie_id)

    if result == None:
        raise HTTPException(status_code=404, detail="Movie not found")

    crud.update_movie(db, movie_id, movie)

    return crud.get_movie(db, movie_id)


@router.delete(
    "/{movie_id}",
    response_model=MovieOut,
    responses={404: {"description": "The movie was not found"}},
)
def delete_movie(
    movie_id: Annotated[
        int,
        Path(title="The ID of the movie", example=1),
    ],
    db: Session = Depends(get_db),
):
    result = crud.get_movie(db, movie_id)

    if result == None:
        raise HTTPException(status_code=404, detail="Movie not found")

    crud.delete_movie(db, result)

    return result
