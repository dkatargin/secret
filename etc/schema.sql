CREATE DATABASE secrets ENCODING 'UTF8';
CREATE TABLE secret (uid UUID, text text, expires timestamp, PRIMARY KEY (uid));
CREATE USER secret_app with encrypted password 'qwerty123';
GRANT ALL PRIVILEGES ON secrets.secret to secret_app;