create database pelago;

CREATE TABLE IF NOT EXISTS packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL ,
    CONSTRAINT package_name_unique UNIQUE (name)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS package_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    version_number VARCHAR(50) NOT NULL,
    publication_date DATETIME,
    title VARCHAR(255),
    description text,
    CONSTRAINT package_id_version_unique UNIQUE (package_id, version_number)
) ENGINE=INNODB;


CREATE TABLE IF NOT EXISTS authors_maintainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    CONSTRAINT author_name_unique UNIQUE (name)
) ENGINE=INNODB;


CREATE TABLE IF NOT EXISTS package_authors_maintainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_versions INT NOT NULL,
    authors_maintainers_id INT NOT NULL,
    role VARCHAR(255) NOT NULL
) ENGINE=INNODB;

