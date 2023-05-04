
DROP TABLE IF EXISTS sources;
CREATE TABLE sources (
	source_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	URL TEXT,
	template TEXT,
	api_key TEXT
);

DROP TABLE IF EXISTS topics;
CREATE TABLE topics (
	topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
	topic TEXT
);

DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE "raw_reviews" (
	"review_id"	INTEGER PRIMARY KEY,
	"source_id", INTEGER,
	"pub_date"	DATETIME,
	"title"	TEXT,
	"review_text"	TEXT,
	"rating"	INTEGER,
	FOREIGN KEY("source_id") REFERENCES sources(source_id)
);

DROP TABLE IF EXISTS cooked_reviews;
CREATE TABLE "cooked_reviews" (
	review_id INTEGER,
	topic_id INTEGER,
	angry INTEGER,
	sentiment INTEGER,
	summary TEXT,
	FOREIGN KEY("review_id") REFERENCES raw_reviews(review_id),
	FOREIGN KEY("topic_id") REFERENCES topics(topic_id)
	
);