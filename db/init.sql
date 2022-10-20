CREATE DATABASE main_db;
CREATE DATABASE particle_db;
CREATE TABLE IF NOT EXISTS public.particles (
name text,
link text , 
data_path text,
date TIMESTAMP
);