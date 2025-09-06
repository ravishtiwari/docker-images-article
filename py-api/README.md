
# IMDb API

A comprehensive FastAPI-based movie management system that replicates IMDb functionality with advanced features including vector similarity search, cloud storage integration, and full-text search capabilities.

## Features

- **Complete CRUD Operations**: Create, read, update, and delete movies
- **Advanced Search**: Full-text search and vector similarity search
- **Filtering**: Filter movies by genre, year, director, rating, and more
- **Vector Embeddings**: Semantic search using sentence transformers
- **Cloud Storage**: AWS S3 and Google Cloud Storage integration for movie images
- **PostgreSQL with pgvector**: Vector database for similarity search
- **Production Ready**: Gunicorn, Docker, comprehensive testing
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Authentication Hooks**: Ready for future auth implementation

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database with pgvector extension
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: SQL toolkit and ORM
- **Pytest**: Testing framework
- **Docker**: Containerization
- **Gunicorn**: WSGI HTTP Server for production
- **Boto3**: AWS SDK for S3 integration
- **Google Cloud Storage**: GCP storage integration
- **Sentence Transformers**: For generating text embeddings

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd py-api
```

2. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
docker-compose run migration
```

5. Access the API:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL with pgvector:
```bash
# Install PostgreSQL and pgvector extension
# Run the initialization script
psql -d imdb_db -f scripts/init_db.sql
```

3. Set environment variables:
```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/imdb_db"
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Movies

- `POST /api/v1/movies/` - Create a new movie
- `GET /api/v1/movies/{movie_id}` - Get a movie by ID
- `GET /api/v1/movies/` - List movies with optional filtering
- `PUT /api/v1/movies/{movie_id}` - Update a movie
- `DELETE /api/v1/movies/{movie_id}` - Delete a movie

### Search

- `GET /api/v1/movies/search/text?q={query}` - Full-text search
- `GET /api/v1/movies/search/similar?movie_id={id}` - Find similar movies

### Filtering Parameters

- `genre`: Filter by genre
- `year`: Filter by release year
- `director`: Filter by director name
- `min_rating`: Minimum IMDb rating
- `max_rating`: Maximum IMDb rating
- `skip`: Pagination offset
- `limit`: Number of results per page

## Data Model

The movie model includes comprehensive IMDb-like data:

- **Basic Info**: Title, original title, release date, runtime
- **Content**: Synopsis, plot, tagline
- **Ratings**: IMDb rating, Metacritic score, Rotten Tomatoes score
- **Financial**: Budget, box office earnings
- **People**: Director, writers, cast with character names
- **Categories**: Genres, languages, countries
- **Production**: Production companies, distributors
- **Technical**: Aspect ratio, sound mix, color
- **Media**: Poster URL, backdrop URL, trailer URL
- **Metadata**: IMDb ID, TMDB ID
- **Vectors**: Title, synopsis, and combined embeddings for similarity search

## Vector Search

The API supports semantic similarity search using sentence transformers:

```python
# Find movies similar to a given movie
GET /api/v1/movies/search/similar?movie_id={id}&limit=10&vector_type=combined
```

Vector types:
- `title`: Search based on movie titles
- `synopsis`: Search based on movie synopses
- `combined`: Search based on title + synopsis (recommended)

## Cloud Storage

### AWS S3 Configuration

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
```

### Google Cloud Storage Configuration

```bash
GCP_PROJECT_ID=your_project_id
GCS_BUCKET_NAME=your_bucket_name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_movie_crud.py

# Run tests with specific markers
pytest -m "not slow"
```

Test categories:
- Unit tests: `pytest -m unit`
- Integration tests: `pytest -m integration`
- Exclude slow tests: `pytest -m "not slow"`

## Production Deployment

### Using Gunicorn

```bash
gunicorn main:app -c gunicorn_conf.py
```

### Using Docker

```bash
docker build -t imdb-api .
docker run -p 8000:8000 imdb-api
```

### Environment Variables

Key environment variables for production:

```bash
DEBUG=false
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-super-secret-key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
GCP_PROJECT_ID=your_gcp_project
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Authentication (Future Implementation)

The API includes authentication hooks that can be easily enabled:

1. Uncomment `@auth_required` decorators in controllers
2. Implement authentication logic in `app/core/auth.py`
3. Add user management endpoints
4. Configure JWT or OAuth2 settings

## Performance Considerations

- **Database Indexing**: Comprehensive indexes on searchable fields
- **Vector Indexes**: IVFFlat indexes for fast similarity search
- **Connection Pooling**: SQLAlchemy connection pooling
- **Caching**: Ready for Redis integration
- **Pagination**: Built-in pagination for large result sets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please open an issue in the GitHub repository.
