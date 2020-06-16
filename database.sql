CREATE TABLE login_signup(
	username VARCHAR NOT NULL,
	password VARCHAR NOT NULL
	);


CREATE TABLE books_des(
	isbn_num int NOT NULL,
	title VARCHAR NOT NULL,
	author VARCHAR NOT NULL,
	publish_year VARCHAR NOT NULL
	);


CREATE TABLE book_reviews(
	username VARCHAR NOT NULL,
	isbn_num VARCHAR NOT NULL,
	rating INT NOT NULL,
	review VARCHAR NOT NULL,
	);


ALTER TABLE books_des ALTER COLUMN isbn_num TYPE CHAR;

ALTER TABLE book_reviews DROP COLUMN rating;