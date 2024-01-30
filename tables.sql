CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOL DEFAULT false
);

-- Ravintolat-taulu
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    location TEXT,
    rating INTEGER,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Arviot-taulu
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    user_id INTEGER REFERENCES users(id),
    review_text TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ryhmät-taulu
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ravintola-ryhmä yhteys -taulu
CREATE TABLE restaurant_group (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    group_id INTEGER REFERENCES groups(id)
);
