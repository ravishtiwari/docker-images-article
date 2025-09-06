import pytest
from datetime import date
from uuid import uuid4

from app.crud.movie import movie_crud
from app.schemas.movie import MovieCreate, MovieUpdate, CastMember


def test_create_movie(db_session):
    """Test creating a new movie"""
    movie_data = MovieCreate(
        title="The Matrix",
        original_title="The Matrix",
        release_date=date(1999, 3, 31),
        runtime=136,
        synopsis="A computer programmer discovers reality is a simulation.",
        director="The Wachowskis",
        genres=["Action", "Sci-Fi"],
        imdb_rating=8.7,
        cast=[
            CastMember(name="Keanu Reeves", character="Neo", order=1),
            CastMember(name="Laurence Fishburne", character="Morpheus", order=2),
        ],
    )

    movie = movie_crud.create(db_session, movie_data)

    assert movie.title == "The Matrix"
    assert movie.director == "The Wachowskis"
    assert movie.imdb_rating == 8.7
    assert len(movie.genres) == 2
    assert movie.search_vector is not None


def test_get_movie(db_session):
    """Test retrieving a movie by ID"""
    movie_data = MovieCreate(
        title="Inception",
        director="Christopher Nolan",
        release_date=date(2010, 7, 16),
        imdb_rating=8.8,
    )

    created_movie = movie_crud.create(db_session, movie_data)
    retrieved_movie = movie_crud.get(db_session, created_movie.id)

    assert retrieved_movie is not None
    assert retrieved_movie.title == "Inception"
    assert retrieved_movie.director == "Christopher Nolan"


def test_get_movie_not_found(db_session):
    """Test retrieving a non-existent movie"""
    non_existent_id = uuid4()
    movie = movie_crud.get(db_session, non_existent_id)
    assert movie is None


def test_update_movie(db_session):
    """Test updating a movie"""
    movie_data = MovieCreate(
        title="The Dark Knight", director="Christopher Nolan", imdb_rating=9.0
    )

    created_movie = movie_crud.create(db_session, movie_data)

    update_data = MovieUpdate(
        synopsis="Batman faces the Joker in Gotham City.", runtime=152
    )

    updated_movie = movie_crud.update(db_session, created_movie.id, update_data)

    assert updated_movie is not None
    assert updated_movie.synopsis == "Batman faces the Joker in Gotham City."
    assert updated_movie.runtime == 152
    assert updated_movie.title == "The Dark Knight"  # Unchanged


def test_delete_movie(db_session):
    """Test deleting a movie"""
    movie_data = MovieCreate(title="Pulp Fiction", director="Quentin Tarantino")

    created_movie = movie_crud.create(db_session, movie_data)
    movie_id = created_movie.id

    # Delete the movie
    success = movie_crud.delete(db_session, movie_id)
    assert success is True

    # Verify it's deleted
    deleted_movie = movie_crud.get(db_session, movie_id)
    assert deleted_movie is None


def test_search_movies(db_session):
    """Test searching movies"""
    movies_data = [
        MovieCreate(title="The Matrix", director="The Wachowskis", genres=["Sci-Fi"]),
        MovieCreate(
            title="Matrix Reloaded", director="The Wachowskis", genres=["Sci-Fi"]
        ),
        MovieCreate(title="Inception", director="Christopher Nolan", genres=["Sci-Fi"]),
    ]

    for movie_data in movies_data:
        movie_crud.create(db_session, movie_data)

    # Search for "Matrix"
    results = movie_crud.search(db_session, "Matrix")
    assert len(results) == 2

    # Search for "Nolan"
    results = movie_crud.search(db_session, "Nolan")
    assert len(results) == 1
    assert results[0].director == "Christopher Nolan"


def test_filter_movies(db_session):
    """Test filtering movies"""
    movies_data = [
        MovieCreate(
            title="Movie A",
            director="Director A",
            genres=["Action"],
            release_date=date(2020, 1, 1),
            imdb_rating=8.0,
        ),
        MovieCreate(
            title="Movie B",
            director="Director B",
            genres=["Comedy"],
            release_date=date(2021, 1, 1),
            imdb_rating=7.5,
        ),
        MovieCreate(
            title="Movie C",
            director="Director A",
            genres=["Action"],
            release_date=date(2020, 6, 1),
            imdb_rating=8.5,
        ),
    ]

    for movie_data in movies_data:
        movie_crud.create(db_session, movie_data)

    # Filter by genre
    action_movies = movie_crud.get_multi(db_session, genre="Action")
    assert len(action_movies) == 2

    # Filter by year
    movies_2020 = movie_crud.get_multi(db_session, year=2020)
    assert len(movies_2020) == 2

    # Filter by director
    director_a_movies = movie_crud.get_multi(db_session, director="Director A")
    assert len(director_a_movies) == 2

    # Filter by rating range
    high_rated_movies = movie_crud.get_multi(db_session, min_rating=8.0)
    assert len(high_rated_movies) == 2


def test_count_movies(db_session):
    """Test counting movies"""
    assert movie_crud.count(db_session) == 0

    movie_data = MovieCreate(title="Test Movie", director="Test Director")
    movie_crud.create(db_session, movie_data)

    assert movie_crud.count(db_session) == 1
