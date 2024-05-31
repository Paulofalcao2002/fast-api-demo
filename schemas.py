from pydantic import BaseModel, Field
from datetime import date as date_type


class BaseMovie(BaseModel):
    name: str = Field(description="The name of the movie", example="Titanic")
    date: date_type = Field(
        description="The release date of the movie", example=date_type(1998, 1, 12)
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Titanic",
                "date": date_type(1998, 1, 12),
            }
        }


class MovieOut(BaseMovie):
    movie_id: int = Field(description="The id of the movie", example=1)

    class Config:
        schema_extra = {
            "example": {
                "movie_id": 1,
                "name": "Titanic",
                "date": date_type(1998, 1, 12),
            }
        }
        orm_mode = True


class BaseRating(BaseModel):
    movie_id: int = Field(
        description="The id of the movie the rating is about", example=1
    )
    value: float = Field(
        description="The value of the rating, in the range from 0 to 5",
        ge=0,
        le=5,
        example=4.5,
    )
    description: str | None = Field(
        default=None,
        description="Description about the rating",
        max_length=500,
        example="That was a really nice movie!",
    )

    class Config:
        schema_extra = {
            "example": {
                "movie_id": 1,
                "value": 4.5,
                "description": "That was a really nice movie!",
            }
        }


class RatingOut(BaseRating):
    rating_id: int = Field(description="The id of the rating", example=1)

    class Config:
        schema_extra = {
            "example": {
                "rating_id": 1,
                "movie_id": 1,
                "value": 4.5,
                "description": "That was a really nice movie!",
            }
        }
        orm_mode = True
