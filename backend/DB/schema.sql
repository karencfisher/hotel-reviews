DROP TABLE IF EXISTS topics;
CREATE TABLE topics (
	category VARCHAR,
	topic_name VARCHAR,
	PRIMARY KEY (category, topic_name)
);

DROP TABLE IF EXISTS sources;
CREATE TABLE sources (
	source_name VARCHAR,
	source_language VARCHAR,
	PRIMARY KEY (source_name, source_language)
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
	locations_location VARCHAR,
	source_name VARCHAR,
	category VARCHAR,
	location_description VARCHAR,
	PRIMARY KEY (locations_location, source_name),
	FOREIGN KEY (source_name) REFERENCES sources(source_name),
	FOREIGN KEY (category) REFERENCES topics(category)
);

DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE raw_reviews (
	review_id	VARCHAR,
	source_name VARCHAR,
	locations_location VARCHAR,
	category VARCHAR,
	pub_date	DATETIME,
	title	VARCHAR,
	review_text	VARCHAR,
	rating	INTEGER,
	reviewed BOOLEAN DEFAULT false,
	PRIMARY KEY (review_id, source_name),
	FOREIGN KEY(source_name) REFERENCES sources(source_name),
	FOREIGN KEY(category, locations_location) REFERENCES locations(category, locations_location),
);

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE cooked_reviews (
	review_id VARCHAR,
	source_name VARCHAR,
	category VARCHAR,
	topic_name VARCHAR,
	angry INTEGER,
	sentiment INTEGER,
	summary VARCHAR,
	PRIMARY KEY (review_id, source_name, topic_name),
	FOREIGN KEY(review_id, source_name) REFERENCES 
		raw_reviews(review_id, source_name),
	FOREIGN KEY(category, topic_name) REFERENCES 
		topics(category, topic_name)
);