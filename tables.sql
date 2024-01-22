-- Käyttäjät
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Ryhmät
CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL
);

-- Ravintolat
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_by_user_id INT REFERENCES users(user_id),
    PRIMARY KEY (restaurant_id)
);

-- Arviot
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    restaurant_id INT REFERENCES restaurants(restaurant_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    PRIMARY KEY (review_id)
);

-- Ryhmien ja ravintoloiden liitostaulu
CREATE TABLE restaurant_groups (
    restaurant_id INT REFERENCES restaurants(restaurant_id),
    group_id INT REFERENCES groups(group_id),
    PRIMARY KEY (restaurant_id, group_id)
);
