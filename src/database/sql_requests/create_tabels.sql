-- Active: 1724139112563@@127.0.0.1@5432@guess_movie
CREATE DATABASE "guess_movie";
 
CREATE TABLE IF NOT EXISTS "films" (
    "id" serial NOT NULL UNIQUE,
    "adult" boolean NOT NULL,
    "backdrop_path" varchar(150),
    "id_tmdb" integer NOT NULL UNIQUE DEFAULT 0,
    "original_language" varchar(50) NOT NULL,
    "title" varchar(100) NOT NULL,
    "overview" varchar(1000),
    "poster_path" varchar(150),
    "release_date" date NOT NULL,
    "vote_average" double precision NOT NULL,
    PRIMARY KEY ("id")
);

-- DROP TABLE IF EXISTS "genres";

CREATE TABLE IF NOT EXISTS "genres" (
    "id" serial NOT NULL UNIQUE,
    "id_tmdb" integer NOT NULL UNIQUE,
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
    "id_tmdb" integer NOT NULL DEFAULT 0 UNIQUE,
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

-- DROP TABLE result;

-- DROP TABLE user_role;

-- DROP TABLE users CASCADE;

CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL PRIMARY KEY,
    "nick" VARCHAR(50) NOT NULL UNIQUE,
    "e_mail" VARCHAR(150) NOT NULL UNIQUE,
    "name" VARCHAR(150) NOT NULL,
    "birthdate" DATE NOT NULL,
    "role_id" INTEGER NOT NULL DEFAULT 1,
    "password" VARCHAR(255) NOT NULL,
    FOREIGN KEY ("role_id") REFERENCES "user_role" ("id")
);

-- DROP TABLE user_role;

CREATE TABLE IF NOT EXISTS "user_role" (
    "id" serial NOT NULL UNIQUE,
    "role" varchar(50) NOT NULL UNIQUE,
    PRIMARY KEY ("id")
);

INSERT INTO "user_role" ("role") VALUES ('user'), ('administrator');

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
    "known_for_department" varchar(100) NOT NULL UNIQUE,
    PRIMARY KEY ("id")
);


-- Creating restrictions with cascading deletion and updating
-- ALTER TABLE known_for_department
-- ADD CONSTRAINT unique_known_for_department UNIQUE (known_for_department);

-- ALTER TABLE people
-- ADD CONSTRAINT id_tmdb_unique UNIQUE (id_tmdb);


ALTER TABLE "genres_films" 
ADD CONSTRAINT "genres_films_fk0" 
FOREIGN KEY ("id_film") REFERENCES "films"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "genres_films" 
ADD CONSTRAINT "genres_films_fk1" 
FOREIGN KEY ("id_genre") REFERENCES "genres"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "keywords" 
ADD CONSTRAINT "keywords_fk2" 
FOREIGN KEY ("id_film") REFERENCES "films"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "people_films" 
ADD CONSTRAINT "people_films_fk1" 
FOREIGN KEY ("id_film") REFERENCES "films"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "people_films" 
ADD CONSTRAINT "people_films_fk2" 
FOREIGN KEY ("id_people") REFERENCES "people"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "people_films" 
ADD CONSTRAINT "people_films_fk3" 
FOREIGN KEY ("id_known_for_department") REFERENCES "known_for_department"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE "guessed_films" 
ADD CONSTRAINT "guessed_films_fk1" 
FOREIGN KEY ("id_film") REFERENCES "films"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "guessed_films" 
ADD CONSTRAINT "guessed_films_fk2" 
FOREIGN KEY ("id_user") REFERENCES "users"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "result" 
ADD CONSTRAINT "result_fk1" 
FOREIGN KEY ("id_user") REFERENCES "users"("id") 
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "genres" 
ADD CONSTRAINT unique_id_tmdb UNIQUE ("id_tmdb");




-- ALTER TABLE films ALTER COLUMN overview TYPE VARCHAR(1000);
-- Removing existing restrictions
-- ALTER TABLE "genres_films" DROP CONSTRAINT "genres_films_fk0";
-- ALTER TABLE "genres_films" DROP CONSTRAINT "genres_films_fk1";
-- ALTER TABLE "keywords" DROP CONSTRAINT "keywords_fk2";
-- ALTER TABLE "people_films" DROP CONSTRAINT "people_films_fk1";
-- ALTER TABLE "people_films" DROP CONSTRAINT "people_films_fk2";
-- ALTER TABLE "people_films" DROP CONSTRAINT "people_films_fk3";
-- ALTER TABLE "users" DROP CONSTRAINT "users_fk5";
-- ALTER TABLE "guessed_films" DROP CONSTRAINT "guessed_films_fk1";
-- ALTER TABLE "guessed_films" DROP CONSTRAINT "guessed_films_fk2";
-- ALTER TABLE "result" DROP CONSTRAINT "result_fk1";