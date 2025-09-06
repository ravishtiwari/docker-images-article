from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..core.database import get_db
from ..handlers.movie_handler import movie_handler
from ..schemas.movie import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieSearchResponse,
    SimilarMovieResponse,
)
from ..core.auth import auth_required  # Placeholder for future auth

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=MovieResponse)
# @auth_required  # Uncomment when auth is implemented
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """Create a new movie"""
    return movie_handler.create_movie(db, movie)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: UUID, db: Session = Depends(get_db)):
    """Get a movie by ID"""
    movie = movie_handler.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/", response_model=MovieSearchResponse)
def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genre: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    director: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=10),
    max_rating: Optional[float] = Query(None, ge=0, le=10),
    db: Session = Depends(get_db),
):
    """Get movies with optional filtering"""
    return movie_handler.get_movies(
        db, skip, limit, genre, year, director, min_rating, max_rating
    )


@router.get("/search/text", response_model=MovieSearchResponse)
def search_movies(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Full-text search for movies"""
    return movie_handler.search_movies(db, q, skip, limit)


@router.get("/search/similar", response_model=List[SimilarMovieResponse])
def find_similar_movies(
    movie_id: UUID,
    limit: int = Query(10, ge=1, le=50),
    vector_type: str = Query("combined", regex="^(title|synopsis|combined)$"),
    db: Session = Depends(get_db),
):
    """Find similar movies using vector similarity"""
    return movie_handler.find_similar_movies(db, movie_id, limit, vector_type)


@router.put("/{movie_id}", response_model=MovieResponse)
# @auth_required  # Uncomment when auth is implemented
def update_movie(
    movie_id: UUID, movie_update: MovieUpdate, db: Session = Depends(get_db)
):
    """Update a movie"""
    movie = movie_handler.update_movie(db, movie_id, movie_update)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.delete("/{movie_id}")
# @auth_required  # Uncomment when auth is implemented
def delete_movie(movie_id: UUID, db: Session = Depends(get_db)):
    """Delete a movie"""
    success = movie_handler.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}


@router.post("/{movie_id}/images/upload")
# @auth_required  # Uncomment when auth is implemented
def upload_movie_image(
    movie_id: UUID,
    image_type: str = Query(..., regex="^(poster|backdrop)$"),
    provider: str = Query("s3", regex="^(s3|gcs)$"),
    db: Session = Depends(get_db),
):
    """Upload movie image to cloud storage"""
    # This endpoint would handle file upload
    # Implementation depends on file upload handling
    return {"message": "Image upload endpoint - implementation needed"}
