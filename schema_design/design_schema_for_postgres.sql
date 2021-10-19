CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;


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
    role character varying(255) NOT NULL,
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
    type  character varying(255) NOT NULL,
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

CREATE INDEX film_work_genre_film_id_idx ON content.genre_film_work(film_work_id);
CREATE INDEX film_work_genre_id_idx ON content.genre_film_work(genre_id);

CREATE INDEX person_film_work_id_idx ON content.person_film_work(film_work_id);
CREATE INDEX film_work_person_id_idx ON content.person_film_work(person_id);
