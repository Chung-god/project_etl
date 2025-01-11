CREATE USER postgres WITH PASSWORD 'postgres_password';
CREATE DATABASE etl_db;
GRANT ALL PRIVILEGES ON DATABASE etl_db TO postgres;

CREATE USER etl_user WITH PASSWORD 'etl_password';
GRANT ALL PRIVILEGES ON DATABASE etl_db TO etl_user;
