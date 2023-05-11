
DROP TABLE IF EXISTS sources;
CREATE TABLE sources (
	source_id INTEGER PRIMARY KEY AUTOINCREMENT,
	source_name VARCHAR UNIQUE,
	source_URL VARCHAR,
	template VARCHAR,
	api_key VARCHAR
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
	locations_location VARCHAR,
	source_name VARCHAR,
	PRIMARY KEY (locations_location, source_name),
	FOREIGN KEY (source_name) REFERENCES sources(source_name)
);

DROP TABLE IF EXISTS topics;
CREATE TABLE topics (
	topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
	topic VARCHAR UNIQUE
);

DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE raw_reviews (
	review_id	VARCHAR,
	source_id, INTEGER,
	pub_date	DATETIME,
	title	VARCHAR,
	review_text	VARCHAR,
	rating	INTEGER,
	reviewed BOOLEAN DEFAULT false,
	PRIMARY KEY (review_id, source_id),
	FOREIGN KEY(source_id) REFERENCES sources(source_id)
);

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE cooked_reviews (
	review_id VARCHAR,
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