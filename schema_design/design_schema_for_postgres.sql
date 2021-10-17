CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;


CREATE TYPE type_movie AS ENUM ('series', 'movie');
CREATE TYPE role AS ENUM ('director', 'actor', 'writer');

CREATE TABLE IF NOT EXISTS content.person(
    id uuid PRIMARY KEY,
    first_name character varying(255) NOT NULL,
    last_name character varying(255),
    patronymic character varying(255),
    birthdate DATE,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role role NOT NULL,
    created_at timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title character varying(255) NOT NULL,
    description TEXT,
    creation_date date,
    rating FLOAT,
    certificate character varying(255),
    file_path TEXT,
    type type_movie NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL,
    description TEXT,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);

CREATE SEQUENCE content.film_work_person_id_seq AS integer;
CREATE SEQUENCE content.film_work_genre_id_seq AS integer;

ALTER SEQUENCE content.film_work_person_id_seq owned BY content.person_film_work.id;
ALTER SEQUENCE content.film_work_genre_id_seq owned BY content.genre_film_work.id;

ALTER TABLE content.person_film_work ALTER column id SET default nextval('content.film_work_person_id_seq'::regclass);
ALTER TABLE content.genre_film_work ALTER column id set default nextval('content.film_work_genre_id_seq'::regclass);
