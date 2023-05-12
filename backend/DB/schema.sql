
DROP TABLE IF EXISTS sources;
CREATE TABLE sources (
	source_name VARCHAR PRIMARY KEY,
	source_URL VARCHAR,
	template VARCHAR,
	source_language VARCHAR,
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
	topic_name VARCHAR PRIMARY KEY
);

DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE raw_reviews (
	review_id	VARCHAR,
	source_name VARCHAR,
	pub_date	DATETIME,
	title	VARCHAR,
	review_text	VARCHAR,
	rating	INTEGER,
	reviewed BOOLEAN DEFAULT false,
	PRIMARY KEY (review_id, source_name),
	FOREIGN KEY(source_name) REFERENCES sources(source_name)
);

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE cooked_reviews (
	review_id VARCHAR,
	source_name VARCHAR,
	topic_name VARCHAR,
	angry INTEGER,
	sentiment INTEGER,
	summary VARCHAR,
	PRIMARY KEY (review_id, source_name, topic_name),
	FOREIGN KEY(review_id, source_name) REFERENCES 
		raw_reviews(review_id, source_name),
	FOREIGN KEY(topic_name) REFERENCES topics(topic_name)
);