import pytest
from datetime import date


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_movie(client):
    """Test creating a movie via API"""
    movie_data = {
        "title": "Test Movie",
        "director": "Test Director",
        "release_date": "2023-01-01",
        "runtime": 120,
        "synopsis": "A test movie for API testing",
        "imdb_rating": 8.0,
        "genres": ["Action", "Drama"],
        "cast": [
            {"name": "Actor One", "character": "Hero", "order": 1},
            {"name": "Actor Two", "character": "Villain", "order": 2},
        ],
    }

    response = client.post("/api/v1/movies/", json=movie_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Movie"
    assert data["director"] == "Test Director"
    assert data["imdb_rating"] == 8.0


def test_get_movie(client):
    """Test retrieving a movie via API"""
    # First create a movie
    movie_data = {"title": "Get Test Movie", "director": "Get Test Director"}

    create_response = client.post("/api/v1/movies/", json=movie_data)
    created_movie = create_response.json()
    movie_id = created_movie["id"]

    # Then retrieve it
    response = client.get(f"/api/v1/movies/{movie_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Get Test Movie"
    assert data["id"] == movie_id


def test_get_movie_not_found(client):
    """Test retrieving a non-existent movie"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/movies/{fake_id}")
    assert response.status_code == 404


def test_update_movie(client):
    """Test updating a movie via API"""
    # Create a movie
    movie_data = {"title": "Update Test Movie", "director": "Update Test Director"}

    create_response = client.post("/api/v1/movies/", json=movie_data)
    created_movie = create_response.json()
    movie_id = created_movie["id"]

    # Update it
    update_data = {"synopsis": "Updated synopsis", "runtime": 150}

    response = client.put(f"/api/v1/movies/{movie_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["synopsis"] == "Updated synopsis"
    assert data["runtime"] == 150
    assert data["title"] == "Update Test Movie"  # Should remain unchanged


def test_delete_movie(client):
    """Test deleting a movie via API"""
    # Create a movie
    movie_data = {"title": "Delete Test Movie", "director": "Delete Test Director"}

    create_response = client.post("/api/v1/movies/", json=movie_data)
    created_movie = create_response.json()
    movie_id = created_movie["id"]

    # Delete it
    response = client.delete(f"/api/v1/movies/{movie_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/api/v1/movies/{movie_id}")
    assert get_response.status_code == 404


def test_search_movies(client):
    """Test searching movies via API"""
    # Create test movies
    movies = [
        {"title": "Search Movie One", "director": "Director A"},
        {"title": "Search Movie Two", "director": "Director B"},
        {"title": "Different Title", "director": "Director A"},
    ]

    for movie in movies:
        client.post("/api/v1/movies/", json=movie)

    # Search for "Search"
    response = client.get("/api/v1/movies/search/text?q=Search")
    assert response.status_code == 200

    data = response.json()
    assert len(data["movies"]) == 2


def test_get_movies_with_filters(client):
    """Test getting movies with filters"""
    # Create test movies
    movies = [
        {
            "title": "Action Movie",
            "director": "Action Director",
            "genres": ["Action"],
            "release_date": "2020-01-01",
            "imdb_rating": 8.0,
        },
        {
            "title": "Comedy Movie",
            "director": "Comedy Director",
            "genres": ["Comedy"],
            "release_date": "2021-01-01",
            "imdb_rating": 7.0,
        },
    ]

    for movie in movies:
        client.post("/api/v1/movies/", json=movie)

    # Filter by genre
    response = client.get("/api/v1/movies/?genre=Action")
    assert response.status_code == 200
    data = response.json()
    assert len(data["movies"]) == 1
    assert data["movies"][0]["title"] == "Action Movie"

    # Filter by year
    response = client.get("/api/v1/movies/?year=2021")
    assert response.status_code == 200
    data = response.json()
    assert len(data["movies"]) == 1
    assert data["movies"][0]["title"] == "Comedy Movie"

    # Filter by rating
    response = client.get("/api/v1/movies/?min_rating=7.5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["movies"]) == 1
    assert data["movies"][0]["imdb_rating"] == 8.0


def test_invalid_movie_data(client):
    """Test creating a movie with invalid data"""
    invalid_data = {
        "title": "",  # Empty title should fail validation
        "imdb_rating": 15.0,  # Rating > 10 should fail validation
    }

    response = client.post("/api/v1/movies/", json=invalid_data)
    assert response.status_code == 422  # Validation error
