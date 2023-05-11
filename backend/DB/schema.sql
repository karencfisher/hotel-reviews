
DROP TABLE IF EXISTS sources;
CREATE TABLE sources (
	source_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR UNIQUE,
	URL VARCHAR,
	template VARCHAR,
	location VARCHAR,
	api_key VARCHAR
);

DROP TABLE IF EXISTS topics;
CREATE TABLE topics (
	topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
	topic VARCHAR UNIQUE
);

DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE raw_reviews (
	review_id	INTEGER,
	source_id, INTEGER,
	pub_date	DATETIME,
	title	VARCHAR,
	review_text	VARCHAR,
	rating	INTEGER,
	PRIMARY KEY (review_id, source_id),
	FOREIGN KEY(source_id) REFERENCES sources(source_id)
);

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE cooked_reviews (
	review_id INTEGER,
	source_id INTEGER,
	topic_id INTEGER,
	angry INTEGER,
	sentiment INTEGER,
	summary VARCHAR,
	PRIMARY KEY (review_id, source_id, topic_id),
	FOREIGN KEY(review_id, source_id) REFERENCES 
		raw_reviews(review_id, source_id),
	FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
);