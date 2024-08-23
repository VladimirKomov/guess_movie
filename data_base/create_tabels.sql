-- Active: 1724139112563@@127.0.0.1@5432@guess_movie
CREATE DATABASE "guess_movie";

CREATE TABLE IF NOT EXISTS "films" (
    "id" serial NOT NULL UNIQUE,
    "adult" boolean NOT NULL,
    "backdrop_path" varchar(150),
    "id_tmdb" integer NOT NULL DEFAULT 0,
    "original_language" varchar(50) NOT NULL,
    "title" varchar(100) NOT NULL,
    "overview" varchar(500),
    "poster_path" varchar(150),
    "release_date" date NOT NULL,
    "vote_average" double precision NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "genres" (
    "id" serial NOT NULL UNIQUE,
    "id_tmdb" integer NOT NULL DEFAULT 0,
    "name" varchar(60) NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "genres_films" (
    "id_film" integer NOT NULL,
    "id_genre" integer NOT NULL,
    UNIQUE ("id_film", "id_genre")
);

CREATE TABLE IF NOT EXISTS "keywords" (
    "id" serial NOT NULL UNIQUE,
    "keywords" varchar(500) NOT NULL,
    "id_film" integer NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "people" (
    "id" serial NOT NULL UNIQUE,
    "id_tmdb" integer NOT NULL DEFAULT 0,
    "name" varchar(80) NOT NULL,
    "gender" smallint NOT NULL,
    "profile_path_photo" varchar(200),
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "people_films" (
    "id" serial NOT NULL UNIQUE,
    "id_film" integer NOT NULL,
    "id_people" integer NOT NULL,
    "id_known_for_department" integer NOT NULL,
    UNIQUE ("id_film", "id_people", "id_known_for_department"),
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "users" (
    "id" serial NOT NULL UNIQUE,
    "nick" varchar(50) NOT NULL UNIQUE,
    "e_mail" varchar(150) NOT NULL UNIQUE,
    "name" varchar(150) NOT NULL,
    "birthdate" date NOT NULL,
    "role" integer NOT NULL,
    "password" varchar(50) NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "user_role" (
    "id" serial NOT NULL UNIQUE,
    "role" varchar(50) NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "guessed_films" (
    "id" serial NOT NULL UNIQUE,
    "id_film" integer NOT NULL,
    "id_user" integer NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "result" (
    "id" serial NOT NULL UNIQUE,
    "id_user" integer NOT NULL,
    "number_games" integer NOT NULL,
    "points" integer NOT NULL,
    "number_wins" integer NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "known_for_department" (
    "id" serial NOT NULL UNIQUE,
    "known_for_department" varchar(100) NOT NULL,
    PRIMARY KEY ("id")
);

ALTER TABLE "genres_films" ADD CONSTRAINT "genres_films_fk0" FOREIGN KEY ("id_film") REFERENCES "films"("id");
ALTER TABLE "genres_films" ADD CONSTRAINT "genres_films_fk1" FOREIGN KEY ("id_genre") REFERENCES "genres"("id");
ALTER TABLE "keywords" ADD CONSTRAINT "keywords_fk2" FOREIGN KEY ("id_film") REFERENCES "films"("id");

ALTER TABLE "people_films" ADD CONSTRAINT "people_films_fk1" FOREIGN KEY ("id_film") REFERENCES "films"("id");
ALTER TABLE "people_films" ADD CONSTRAINT "people_films_fk2" FOREIGN KEY ("id_people") REFERENCES "people"("id");
ALTER TABLE "people_films" ADD CONSTRAINT "people_films_fk3" FOREIGN KEY ("id_known_for_department") REFERENCES "known_for_department"("id");

ALTER TABLE "users" ADD CONSTRAINT "users_fk5" FOREIGN KEY ("role") REFERENCES "user_role"("id");

ALTER TABLE "guessed_films" ADD CONSTRAINT "guessed_films_fk1" FOREIGN KEY ("id_film") REFERENCES "films"("id");
ALTER TABLE "guessed_films" ADD CONSTRAINT "guessed_films_fk2" FOREIGN KEY ("id_user") REFERENCES "users"("id");

ALTER TABLE "result" ADD CONSTRAINT "result_fk1" FOREIGN KEY ("id_user") REFERENCES "users"("id");
