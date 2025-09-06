from sqlalchemy import Column, Integer, String, Text, Float, Date, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from ..core.database import Base
import uuid


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    original_title = Column(String(255))
    release_date = Column(Date)
    runtime = Column(Integer)  # in minutes

    # Content
    synopsis = Column(Text)
    plot = Column(Text)
    tagline = Column(String(500))

    # Ratings and Reviews
    imdb_rating = Column(Float)
    metacritic_score = Column(Integer)
    rotten_tomatoes_score = Column(Integer)

    # Financial
    budget = Column(Integer)  # in USD
    box_office = Column(Integer)  # in USD

    # People
    director = Column(String(255))
    writers = Column(ARRAY(String))
    cast = Column(
        JSON
    )  # [{"name": "Actor Name", "character": "Character Name", "order": 1}]

    # Categories
    genres = Column(ARRAY(String))
    languages = Column(ARRAY(String))
    countries = Column(ARRAY(String))

    # Production
    production_companies = Column(ARRAY(String))
    distributors = Column(ARRAY(String))

    # Technical
    aspect_ratio = Column(String(50))
    sound_mix = Column(ARRAY(String))
    color = Column(String(50))

    # Media
    poster_url = Column(String(500))
    backdrop_url = Column(String(500))
    trailer_url = Column(String(500))

    # Metadata
    imdb_id = Column(String(20), unique=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True)

    # Vector embeddings for similarity search
    title_vector = Column(Vector(384))
    synopsis_vector = Column(Vector(384))
    combined_vector = Column(Vector(384))

    # Search
    search_vector = Column(Text)  # For full-text search
