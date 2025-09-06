from sqlalchemy.orm import Session
from sqlalchemy import text, func, or_
from typing import List, Optional
from uuid import UUID
import numpy as np

from ..models.movie import Movie
from ..schemas.movie import MovieCreate, MovieUpdate


class MovieCRUD:

    def create(self, db: Session, movie_data: MovieCreate) -> Movie:
        db_movie = Movie(**movie_data.model_dump(exclude_unset=True))

        # Generate search vector for full-text search
        search_text = f"{movie_data.title or ''} {movie_data.synopsis or ''} {movie_data.director or ''}"
        if movie_data.cast:
            cast_names = " ".join([member.name for member in movie_data.cast])
            search_text += f" {cast_names}"
        if movie_data.genres:
            search_text += f" {' '.join(movie_data.genres)}"

        db_movie.search_vector = search_text

        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    def get(self, db: Session, movie_id: UUID) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.id == movie_id).first()

    def get_by_imdb_id(self, db: Session, imdb_id: str) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.imdb_id == imdb_id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        director: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
    ) -> List[Movie]:
        query = db.query(Movie)

        if genre:
            query = query.filter(Movie.genres.contains([genre]))
        if year:
            query = query.filter(func.extract("year", Movie.release_date) == year)
        if director:
            query = query.filter(Movie.director.ilike(f"%{director}%"))
        if min_rating:
            query = query.filter(Movie.imdb_rating >= min_rating)
        if max_rating:
            query = query.filter(Movie.imdb_rating <= max_rating)

        return query.offset(skip).limit(limit).all()

    def search(
        self, db: Session, query: str, skip: int = 0, limit: int = 100
    ) -> List[Movie]:
        search_terms = query.split()
        conditions = []

        for term in search_terms:
            term_condition = or_(
                Movie.title.ilike(f"%{term}%"),
                Movie.synopsis.ilike(f"%{term}%"),
                Movie.director.ilike(f"%{term}%"),
                Movie.search_vector.ilike(f"%{term}%"),
            )
            conditions.append(term_condition)

        if conditions:
            return (
                db.query(Movie).filter(or_(*conditions)).offset(skip).limit(limit).all()
            )
        return []

    def vector_search(
        self,
        db: Session,
        query_vector: List[float],
        limit: int = 10,
        vector_type: str = "combined",
    ) -> List[tuple]:
        vector_column = getattr(Movie, f"{vector_type}_vector")

        # Convert list to string format for pgvector
        vector_str = f"[{','.join(map(str, query_vector))}]"

        result = db.execute(
            text(
                f"""
                SELECT *, ({vector_column.name} <=> :query_vector) as distance
                FROM movies 
                WHERE {vector_column.name} IS NOT NULL
                ORDER BY {vector_column.name} <=> :query_vector
                LIMIT :limit
            """
            ),
            {"query_vector": vector_str, "limit": limit},
        )

        return result.fetchall()

    def update(
        self, db: Session, movie_id: UUID, movie_update: MovieUpdate
    ) -> Optional[Movie]:
        db_movie = self.get(db, movie_id)
        if not db_movie:
            return None

        update_data = movie_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_movie, field, value)

        # Update search vector if relevant fields changed
        if any(
            field in update_data
            for field in ["title", "synopsis", "director", "cast", "genres"]
        ):
            search_text = f"{db_movie.title or ''} {db_movie.synopsis or ''} {db_movie.director or ''}"
            if db_movie.cast:
                cast_names = " ".join(
                    [member.get("name", "") for member in db_movie.cast]
                )
                search_text += f" {cast_names}"
            if db_movie.genres:
                search_text += f" {' '.join(db_movie.genres)}"
            db_movie.search_vector = search_text

        db.commit()
        db.refresh(db_movie)
        return db_movie

    def delete(self, db: Session, movie_id: UUID) -> bool:
        db_movie = self.get(db, movie_id)
        if not db_movie:
            return False

        db.delete(db_movie)
        db.commit()
        return True

    def count(self, db: Session) -> int:
        return db.query(Movie).count()


movie_crud = MovieCRUD()
