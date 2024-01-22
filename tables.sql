-- Käyttäjä jutut

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);



-- Ravintola jutut

CREATE TABLE restaraunts (
    restaraunt_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_by_user_id INT REFERENCES users(user_id),
    PRIMARY KEY (restaraunt_id)
);


CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL
);


CREATE TABLE restaraunt_groups (
    restaraunt_id INT REFERENCES restaraunts(restaraunt_id),
    group_id INT REFERENCES groups(group_id),
    PRIMARY KEY (restaraunt_id, group_id)
);


CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    restaraunt_id INT REFERENCES restaraunts(restaraunt_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    PRIMARY KEY (review_id)
);

