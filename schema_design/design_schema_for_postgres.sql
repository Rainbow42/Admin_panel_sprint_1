CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS content.actors(
    id uuid PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content.movie_actors (
    movie_id uuid NOT NULL,
    actor_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS content.movies (
    id uuid PRIMARY KEY,
    title character varying(255) NOT NULL,
    plot TEXT,
    imdb_rating FLOAT,
    ratings smallint,
    genre TEXT
);

CREATE TABLE IF NOT EXISTS content.rating_agency (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS content.writers (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS content.movie_writers (
    movie_id uuid NOT NULL,
    writers_id uuid NOT NULL
);

