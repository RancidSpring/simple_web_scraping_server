DROP TABLE IF EXISTS sreality;

CREATE TABLE sreality (
    id SERIAL PRIMARY KEY,
    title character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    image character varying(255) NOT NULL,
    prices character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);