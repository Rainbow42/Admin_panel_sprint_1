CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;


CREATE TYPE type_movie AS ENUM ('series', 'film');
CREATE TYPE type_person AS ENUM ('directions', 'actors', 'writers');

CREATE TABLE IF NOT EXISTS content.person(
    id uuid PRIMARY KEY,
    first_name character varying(255) NOT NULL,
    last_name character varying(255),
    patronymic character varying(255),
    birthdate DATE  NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work_persons_type (
    id integer PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    type_person type_person NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title character varying(255) NOT NULL,
    description TEXT,
    imdb_rating FLOAT,
    ratings varchar,
    type type_movie NOT NULL
);


CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    title character varying(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work_genre (
    id integer PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL
);

CREATE SEQUENCE content.film_work_person_id_seq AS integer;
CREATE SEQUENCE content.film_work_genre_id_seq AS integer;

ALTER SEQUENCE content.film_work_person_id_seq owned BY content.film_work_persons_type.id;
ALTER SEQUENCE content.film_work_genre_id_seq owned BY content.film_work_genre.id;

ALTER TABLE content.film_work_persons_type ALTER column id SET default nextval('content.film_work_person_id_seq'::regclass);
ALTER TABLE content.film_work_genre ALTER column id set default nextval('content.film_work_genre_id_seq'::regclass);
