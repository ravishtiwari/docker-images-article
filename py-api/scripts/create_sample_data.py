#!/usr/bin/env python3
"""
Script to create sample movie data for testing and development
"""

import sys
import os
from datetime import date

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.schemas.movie import MovieCreate, CastMember
from app.crud.movie import movie_crud


def create_sample_movies():
    """Create sample movie data"""

    sample_movies = [
        MovieCreate(
            title="The Matrix",
            original_title="The Matrix",
            release_date=date(1999, 3, 31),
            runtime=136,
            synopsis="A computer programmer discovers that reality as he knows it is a simulation controlled by machines, and joins a rebellion to free humanity.",
            plot="Neo, a computer programmer, is contacted by the mysterious Morpheus who reveals that the world Neo knows is actually a computer simulation called the Matrix. Neo joins a group of rebels fighting to free humanity from machine control.",
            tagline="The fight for the future begins.",
            imdb_rating=8.7,
            metacritic_score=73,
            budget=63000000,
            box_office=467200000,
            director="The Wachowskis",
            writers=["The Wachowskis"],
            cast=[
                CastMember(name="Keanu Reeves", character="Neo", order=1),
                CastMember(name="Laurence Fishburne", character="Morpheus", order=2),
                CastMember(name="Carrie-Anne Moss", character="Trinity", order=3),
                CastMember(name="Hugo Weaving", character="Agent Smith", order=4),
            ],
            genres=["Action", "Sci-Fi"],
            languages=["English"],
            countries=["United States"],
            production_companies=["Warner Bros.", "Village Roadshow Pictures"],
            aspect_ratio="2.39:1",
            color="Color",
            imdb_id="tt0133093",
        ),
        MovieCreate(
            title="Inception",
            release_date=date(2010, 7, 16),
            runtime=148,
            synopsis="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            plot="Dom Cobb is a skilled thief who specializes in extraction, stealing secrets from people's subconscious minds while they dream. He's offered a chance to have his criminal record erased in exchange for performing an 'inception' - planting an idea rather than stealing one.",
            tagline="Your mind is the scene of the crime.",
            imdb_rating=8.8,
            metacritic_score=74,
            budget=160000000,
            box_office=836800000,
            director="Christopher Nolan",
            writers=["Christopher Nolan"],
            cast=[
                CastMember(name="Leonardo DiCaprio", character="Dom Cobb", order=1),
                CastMember(name="Marion Cotillard", character="Mal", order=2),
                CastMember(name="Tom Hardy", character="Eames", order=3),
                CastMember(name="Ellen Page", character="Ariadne", order=4),
            ],
            genres=["Action", "Sci-Fi", "Thriller"],
            languages=["English", "Japanese", "French"],
            countries=["United States", "United Kingdom"],
            production_companies=["Warner Bros.", "Legendary Entertainment"],
            aspect_ratio="2.39:1",
            color="Color",
            imdb_id="tt1375666",
        ),
        MovieCreate(
            title="The Dark Knight",
            release_date=date(2008, 7, 18),
            runtime=152,
            synopsis="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            plot="Batman, Gordon and Harvey Dent are forced to deal with the chaos unleashed by an anarchist mastermind known only as the Joker, as it drives each of them to their limits.",
            tagline="Why so serious?",
            imdb_rating=9.0,
            metacritic_score=84,
            budget=185000000,
            box_office=1004900000,
            director="Christopher Nolan",
            writers=["Jonathan Nolan", "Christopher Nolan"],
            cast=[
                CastMember(
                    name="Christian Bale", character="Bruce Wayne / Batman", order=1
                ),
                CastMember(name="Heath Ledger", character="The Joker", order=2),
                CastMember(
                    name="Aaron Eckhart", character="Harvey Dent / Two-Face", order=3
                ),
                CastMember(name="Michael Caine", character="Alfred", order=4),
            ],
            genres=["Action", "Crime", "Drama"],
            languages=["English", "Mandarin"],
            countries=["United States", "United Kingdom"],
            production_companies=[
                "Warner Bros.",
                "Legendary Entertainment",
                "DC Comics",
            ],
            aspect_ratio="2.39:1",
            color="Color",
            imdb_id="tt0468569",
        ),
        MovieCreate(
            title="Pulp Fiction",
            release_date=date(1994, 10, 14),
            runtime=154,
            synopsis="The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            plot="A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in this sprawling, comedic crime caper.",
            tagline="Girls like me don't make invitations like this to just anyone.",
            imdb_rating=8.9,
            metacritic_score=94,
            budget=8000000,
            box_office=214200000,
            director="Quentin Tarantino",
            writers=["Quentin Tarantino", "Roger Avary"],
            cast=[
                CastMember(name="John Travolta", character="Vincent Vega", order=1),
                CastMember(
                    name="Samuel L. Jackson", character="Jules Winnfield", order=2
                ),
                CastMember(name="Uma Thurman", character="Mia Wallace", order=3),
                CastMember(name="Bruce Willis", character="Butch Coolidge", order=4),
            ],
            genres=["Crime", "Drama"],
            languages=["English", "Spanish", "French"],
            countries=["United States"],
            production_companies=["Miramax", "A Band Apart"],
            aspect_ratio="2.35:1",
            color="Color",
            imdb_id="tt0110912",
        ),
        MovieCreate(
            title="The Shawshank Redemption",
            release_date=date(1994, 9, 23),
            runtime=142,
            synopsis="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            plot="Andy Dufresne, a banker wrongly convicted of murdering his wife and her lover, is sentenced to life in Shawshank State Penitentiary. Over the years, he befriends fellow inmate Ellis 'Red' Redding and becomes instrumental in money laundering operations.",
            tagline="Fear can hold you prisoner. Hope can set you free.",
            imdb_rating=9.3,
            metacritic_score=80,
            budget=25000000,
            box_office=16000000,
            director="Frank Darabont",
            writers=["Stephen King", "Frank Darabont"],
            cast=[
                CastMember(name="Tim Robbins", character="Andy Dufresne", order=1),
                CastMember(
                    name="Morgan Freeman", character="Ellis Boyd 'Red' Redding", order=2
                ),
                CastMember(name="Bob Gunton", character="Warden Norton", order=3),
                CastMember(name="James Whitmore", character="Brooks Hatlen", order=4),
            ],
            genres=["Drama"],
            languages=["English"],
            countries=["United States"],
            production_companies=["Castle Rock Entertainment"],
            aspect_ratio="1.85:1",
            color="Color",
            imdb_id="tt0111161",
        ),
    ]

    db = SessionLocal()
    try:
        print("Creating sample movies...")
        for movie_data in sample_movies:
            existing_movie = movie_crud.get_by_imdb_id(db, movie_data.imdb_id)
            if existing_movie:
                print(f"Movie '{movie_data.title}' already exists, skipping...")
                continue

            movie = movie_crud.create(db, movie_data)
            print(f"Created movie: {movie.title} (ID: {movie.id})")

        print(f"\nSample data creation completed!")
        print(f"Total movies in database: {movie_crud.count(db)}")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized.")

    create_sample_movies()
