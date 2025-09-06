
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_movies_synopsis ON movies USING gin(to_tsvector('english', synopsis));
CREATE INDEX IF NOT EXISTS idx_movies_director ON movies (director);
CREATE INDEX IF NOT EXISTS idx_movies_release_date ON movies (release_date);
CREATE INDEX IF NOT EXISTS idx_movies_imdb_rating ON movies (imdb_rating);
CREATE INDEX IF NOT EXISTS idx_movies_genres ON movies USING gin(genres);
CREATE INDEX IF NOT EXISTS idx_movies_imdb_id ON movies (imdb_id);
CREATE INDEX IF NOT EXISTS idx_movies_tmdb_id ON movies (tmdb_id);

-- Vector similarity search indexes
CREATE INDEX IF NOT EXISTS idx_movies_title_vector ON movies USING ivfflat (title_vector vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_movies_synopsis_vector ON movies USING ivfflat (synopsis_vector vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_movies_combined_vector ON movies USING ivfflat (combined_vector vector_cosine_ops) WITH (lists = 100);
