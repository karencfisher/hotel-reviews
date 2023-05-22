UPDATE raw_reviews SET reviewed = false;

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE cooked_reviews (
	review_id VARCHAR,
	source_name VARCHAR,
	category VARCHAR,
	locations_location VARCHAR,
	topic_name VARCHAR,
	angry INTEGER,
	sentiment INTEGER,
	summary VARCHAR,
	PRIMARY KEY (review_id, source_name, topic_name),
	FOREIGN KEY(review_id, source_name, locations_location) REFERENCES 
		raw_reviews(review_id, source_name, locations_location),
	FOREIGN KEY(category, topic_name) REFERENCES 
		topics(category, topic_name)
);