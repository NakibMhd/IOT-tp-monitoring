CREATE DATABASE IF NOT EXISTS tp_monitoring;
use tp_monitoring;

CREATE TABLE  IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(500),
    password VARCHAR(200),
    is_admin BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE  IF NOT EXISTS websites (
    id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(200),
    statut BOOLEAN,
    PRIMARY KEY (id)
);

INSERT INTO users (email, password, is_admin) VALUES ('nakib@nakib.fr', '$argon2i$v=19$m=512,t=2,p=2$5Nz7X6uV0nrPmZMSIgSg1A$fh+I3ILj7+jCFT75DbPw/A', true);
INSERT INTO websites (url, statut) VALUES ('https://www.twitter.com', true);
INSERT INTO websites (url, statut) VALUES ('https://www.facebook.com', true);