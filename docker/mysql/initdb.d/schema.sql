CREATE TABLE requests(
    record_id VARCHAR(255),
    record JSON,
    count INT UNSIGNED,
    PRIMARY KEY (record_id)
);