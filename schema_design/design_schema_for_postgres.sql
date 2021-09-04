CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS content.person(
    id uuid PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work_person (
    id integer PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title character varying(255) NOT NULL,
    plot TEXT,
    director TEXT,
    imdb_rating FLOAT,
    ratings varchar
);

CREATE TABLE IF NOT EXISTS content.rating_agency (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work_genre (
    id integer PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS content.writer (
    id uuid PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS content.film_work_writers (
    id integer PRIMARY KEY,
    film_work_id uuid NOT NULL,
    writer_id uuid NOT NULL
);

CREATE SEQUENCE content.film_work_person_id_seq
	AS integer;

ALTER TABLE content.film_work_person ALTER column id SET default nextval('content.film_work_person_id_seq'::regclass);

ALTER SEQUENCE content.film_work_person_id_seq owned BY content.film_work_person.id;

CREATE SEQUENCE content.film_work_writers_id_seq AS integer;

ALTER TABLE content.film_work_writers ALTER column id SET default nextval('content.film_work_writers_id_seq'::regclass);

ALTER SEQUENCE content.film_work_writers_id_seq owned BY content.film_work_writers.id;

CREATE SEQUENCE content.film_work_genre_id_seq AS integer;

ALTER TABLE content.film_work_genre ALTER column id set default nextval('content.film_work_genre_id_seq'::regclass);

ALTER SEQUENCE content.film_work_genre_id_seq owned BY content.film_work_genre.id;

