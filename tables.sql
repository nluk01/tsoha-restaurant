-- KÄYTTÄJÄT
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN DEFAULT false
);

-- RAFLAT
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    opening_hours TEXT,
    description TEXT,
    location TEXT,
    rating INTEGER,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ARVOSTELUT
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    user_id INTEGER REFERENCES users(id),
    review_text TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    average_rating DOUBLE PRECISION 
);

-- RYHMÄT
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RAFLA-RYHMÄ SIDOS
CREATE TABLE restaurant_group (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    group_id INTEGER REFERENCES groups(id)
);
