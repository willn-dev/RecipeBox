--
-- PostgreSQL database dump
--



-- Dumped from database version 16.13 (Homebrew)
-- Dumped by pg_dump version 16.13 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: preparations; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.preparations AS ENUM (
    'fresh',
    'frozen',
    'grated',
    'chopped',
    'sliced',
    'diced',
    'ground',
    'minced',
    'dried',
    'raw',
    'whole'
);


--
-- Name: units; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.units AS ENUM (
    'tsp',
    'Tbsp',
    'C',
    'pt',
    'qt',
    'gal',
    'g',
    'kg',
    'mg',
    'oz',
    'fl_oz'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ingredients (
    ingredient_id integer NOT NULL,
    name character varying(255)
);


--
-- Name: ingredients_ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ingredients ALTER COLUMN ingredient_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ingredients_ingredient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: recipes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recipes (
    recipe_id integer NOT NULL,
    name character varying(255),
    instructions text
);


--
-- Name: recipes_ingredients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recipes_ingredients (
    recipe_id integer,
    ingredient_id integer,
    quantity text
);


--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.recipes ALTER COLUMN recipe_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.recipes_recipe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (ingredient_id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (recipe_id);


--
-- Name: ingredients unique_ing_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT unique_ing_name UNIQUE (name);


--
-- Name: recipes_ingredients recipes_ingredients_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recipes_ingredients
    ADD CONSTRAINT recipes_ingredients_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(ingredient_id);


--
-- Name: recipes_ingredients recipes_ingredients_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recipes_ingredients
    ADD CONSTRAINT recipes_ingredients_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(recipe_id) ON DELETE CASCADE;


--
-- Name: TABLE ingredients; Type: ACL; Schema: public; Owner: -
--

GRANT ALL ON TABLE public.ingredients TO admin;


--
-- Name: TABLE recipes; Type: ACL; Schema: public; Owner: -
--

GRANT ALL ON TABLE public.recipes TO admin;


--
-- Name: TABLE recipes_ingredients; Type: ACL; Schema: public; Owner: -
--

GRANT ALL ON TABLE public.recipes_ingredients TO admin;


--
-- PostgreSQL database dump complete
--



