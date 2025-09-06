from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from uuid import UUID


class CastMember(BaseModel):
    name: str
    character: str
    order: int


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    original_title: Optional[str] = Field(None, max_length=255)
    release_date: Optional[date] = None
    runtime: Optional[int] = Field(None, gt=0)
    synopsis: Optional[str] = None
    plot: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=500)
    imdb_rating: Optional[float] = Field(None, ge=0, le=10)
    metacritic_score: Optional[int] = Field(None, ge=0, le=100)
    rotten_tomatoes_score: Optional[int] = Field(None, ge=0, le=100)
    budget: Optional[int] = Field(None, ge=0)
    box_office: Optional[int] = Field(None, ge=0)
    director: Optional[str] = Field(None, max_length=255)
    writers: Optional[List[str]] = []
    cast: Optional[List[CastMember]] = []
    genres: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    countries: Optional[List[str]] = []
    production_companies: Optional[List[str]] = []
    distributors: Optional[List[str]] = []
    aspect_ratio: Optional[str] = Field(None, max_length=50)
    sound_mix: Optional[List[str]] = []
    color: Optional[str] = Field(None, max_length=50)
    poster_url: Optional[str] = Field(None, max_length=500)
    backdrop_url: Optional[str] = Field(None, max_length=500)
    trailer_url: Optional[str] = Field(None, max_length=500)
    imdb_id: Optional[str] = Field(None, max_length=20)
    tmdb_id: Optional[int] = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    original_title: Optional[str] = Field(None, max_length=255)
    release_date: Optional[date] = None
    runtime: Optional[int] = Field(None, gt=0)
    synopsis: Optional[str] = None
    plot: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=500)
    imdb_rating: Optional[float] = Field(None, ge=0, le=10)
    metacritic_score: Optional[int] = Field(None, ge=0, le=100)
    rotten_tomatoes_score: Optional[int] = Field(None, ge=0, le=100)
    budget: Optional[int] = Field(None, ge=0)
    box_office: Optional[int] = Field(None, ge=0)
    director: Optional[str] = Field(None, max_length=255)
    writers: Optional[List[str]] = None
    cast: Optional[List[CastMember]] = None
    genres: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    production_companies: Optional[List[str]] = None
    distributors: Optional[List[str]] = None
    aspect_ratio: Optional[str] = Field(None, max_length=50)
    sound_mix: Optional[List[str]] = None
    color: Optional[str] = Field(None, max_length=50)
    poster_url: Optional[str] = Field(None, max_length=500)
    backdrop_url: Optional[str] = Field(None, max_length=500)
    trailer_url: Optional[str] = Field(None, max_length=500)
    imdb_id: Optional[str] = Field(None, max_length=20)
    tmdb_id: Optional[int] = None


class MovieResponse(MovieBase):
    id: UUID
    search_vector: Optional[str] = None

    class Config:
        from_attributes = True


class MovieSearchResponse(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    size: int
    total_pages: int


class SimilarMovieResponse(BaseModel):
    movie: MovieResponse
    similarity_score: float
