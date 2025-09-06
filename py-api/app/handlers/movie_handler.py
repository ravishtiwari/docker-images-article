from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import logging

from ..crud.movie import movie_crud
from ..schemas.movie import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieSearchResponse,
    SimilarMovieResponse,
)
from ..services.vector_service import vector_service

logger = logging.getLogger(__name__)


class MovieHandler:

    def create_movie(self, db: Session, movie_data: MovieCreate) -> MovieResponse:
        """Create a new movie with vector embeddings"""
        try:
            # Create movie
            db_movie = movie_crud.create(db, movie_data)

            # Generate and store vector embeddings
            if movie_data.title:
                title_vector = vector_service.generate_embedding(movie_data.title)
                db_movie.title_vector = title_vector

            if movie_data.synopsis:
                synopsis_vector = vector_service.generate_embedding(movie_data.synopsis)
                db_movie.synopsis_vector = synopsis_vector

            # Combined vector for title + synopsis
            if movie_data.title and movie_data.synopsis:
                combined_text = f"{movie_data.title} {movie_data.synopsis}"
                combined_vector = vector_service.generate_embedding(combined_text)
                db_movie.combined_vector = combined_vector

            db.commit()
            db.refresh(db_movie)

            return MovieResponse.model_validate(db_movie)
        except Exception as e:
            logger.error(f"Error creating movie: {e}")
            db.rollback()
            raise

    def get_movie(self, db: Session, movie_id: UUID) -> Optional[MovieResponse]:
        """Get a movie by ID"""
        db_movie = movie_crud.get(db, movie_id)
        if db_movie:
            return MovieResponse.model_validate(db_movie)
        return None

    def get_movies(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        director: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
    ) -> MovieSearchResponse:
        """Get movies with filtering"""
        movies = movie_crud.get_multi(
            db, skip, limit, genre, year, director, min_rating, max_rating
        )
        total = movie_crud.count(db)

        return MovieSearchResponse(
            movies=[MovieResponse.model_validate(movie) for movie in movies],
            total=total,
            page=skip // limit + 1,
            size=len(movies),
            total_pages=(total + limit - 1) // limit,
        )

    def search_movies(
        self, db: Session, query: str, skip: int = 0, limit: int = 100
    ) -> MovieSearchResponse:
        """Full-text search for movies"""
        movies = movie_crud.search(db, query, skip, limit)

        return MovieSearchResponse(
            movies=[MovieResponse.model_validate(movie) for movie in movies],
            total=len(movies),
            page=skip // limit + 1,
            size=len(movies),
            total_pages=1,  # Simplified for search results
        )

    def find_similar_movies(
        self,
        db: Session,
        movie_id: UUID,
        limit: int = 10,
        vector_type: str = "combined",
    ) -> List[SimilarMovieResponse]:
        """Find similar movies using vector similarity"""
        # Get the reference movie
        reference_movie = movie_crud.get(db, movie_id)
        if not reference_movie:
            return []

        # Get the reference vector
        reference_vector = getattr(reference_movie, f"{vector_type}_vector")
        if not reference_vector:
            return []

        # Find similar movies
        similar_results = movie_crud.vector_search(
            db, reference_vector, limit + 1, vector_type  # +1 to exclude self
        )

        similar_movies = []
        for result in similar_results:
            if str(result.id) != str(movie_id):  # Exclude the reference movie
                similarity_score = (
                    1.0 - result.distance
                )  # Convert distance to similarity
                movie_response = MovieResponse.model_validate(result)
                similar_movies.append(
                    SimilarMovieResponse(
                        movie=movie_response, similarity_score=similarity_score
                    )
                )

        return similar_movies[:limit]

    def update_movie(
        self, db: Session, movie_id: UUID, movie_update: MovieUpdate
    ) -> Optional[MovieResponse]:
        """Update a movie"""
        try:
            db_movie = movie_crud.update(db, movie_id, movie_update)
            if not db_movie:
                return None

            # Update vector embeddings if relevant fields changed
            update_data = movie_update.model_dump(exclude_unset=True)

            if "title" in update_data and db_movie.title:
                title_vector = vector_service.generate_embedding(db_movie.title)
                db_movie.title_vector = title_vector

            if "synopsis" in update_data and db_movie.synopsis:
                synopsis_vector = vector_service.generate_embedding(db_movie.synopsis)
                db_movie.synopsis_vector = synopsis_vector

            if (
                ("title" in update_data or "synopsis" in update_data)
                and db_movie.title
                and db_movie.synopsis
            ):
                combined_text = f"{db_movie.title} {db_movie.synopsis}"
                combined_vector = vector_service.generate_embedding(combined_text)
                db_movie.combined_vector = combined_vector

            db.commit()
            db.refresh(db_movie)

            return MovieResponse.model_validate(db_movie)
        except Exception as e:
            logger.error(f"Error updating movie: {e}")
            db.rollback()
            raise

    def delete_movie(self, db: Session, movie_id: UUID) -> bool:
        """Delete a movie"""
        return movie_crud.delete(db, movie_id)


movie_handler = MovieHandler()
