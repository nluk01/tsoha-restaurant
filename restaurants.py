from sqlalchemy import text
from db import db


# Lisää uusi ravintola
def add_restaurant(name, description, location, groups):
    try:
        sql = text("INSERT INTO restaurants (name, description, location) VALUES (:name, :description, :location) RETURNING id")
        result = db.session.execute(sql, {"name": name, "description": description, "location": location})
        restaurant_id = result.fetchone()[0]
        update_restaurant_groups(restaurant_id, groups)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding restaurant: {e}")
        return False
    

# Poista ravintola
def delete_restaurant(restaurant_id):
    try:
        delete_sql = text("DELETE FROM restaurant_group WHERE restaurant_id = :restaurant_id")
        db.session.execute(delete_sql, {"restaurant_id": restaurant_id})        
        sql = text("DELETE FROM restaurants WHERE id = :id")
        db.session.execute(sql, {"id": restaurant_id})        
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error deleting restaurant: {e}")
        return False
    
    
# Päivitä ravintola
def update_restaurant(restaurant_id, name, description, location, groups):
    try:
        sql = text("UPDATE restaurants SET name=:name, description=:description, location=:location WHERE id=:id")
        db.session.execute(sql, {"name": name, "description": description, "location": location, "id": restaurant_id})
        if update_restaurant_groups(restaurant_id, groups):
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating restaurant: {e}")
        return False


# Ravintolan tulostushommat
def get_restaurant_by_id(restaurant_id):
    try:
        sql = text("SELECT * FROM restaurants WHERE id = :id")
        result = db.session.execute(sql, {"id": restaurant_id})
        restaurant = result.fetchone()
        return restaurant
    except Exception as e:
        print(f"Error fetching restaurant: {e}")
        return None

    
def get_all_restaurants():
    try:
        sql = text("""
            SELECT r.id, r.name, r.description, r.location, ARRAY_AGG(g.name) AS groups
            FROM restaurants r
            LEFT JOIN restaurant_group rg ON r.id = rg.restaurant_id
            LEFT JOIN groups g ON rg.group_id = g.id
            GROUP BY r.id, r.name, r.description, r.location
        """)
        result = db.session.execute(sql)
        restaurants = []
        for row in result:
            restaurant = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'location': row[3],
                'groups': row[4] if row[4] else []  
            }
            restaurants.append(restaurant)
        return restaurants
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return []
    




# Lisää uusi ryhmä
def add_group(name, created_by):
    try:
        sql = text("INSERT INTO groups (name, created_by) VALUES (:name, :created_by)")
        db.session.execute(sql, {"name": name, "created_by" :created_by})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding group: {e}")
        return False
    

#Ryhmien tulostushommat
def get_all_groups():
    try:
        sql = text("SELECT * FROM groups")
        result = db.session.execute(sql)
        groups = result.fetchall()
        return groups
    except Exception as e:
        print(f"Error fetching groups: {e}")
        return []
    

#RAVINTOLA-RYHMÄ liitos hommat
def add_restaurant_to_group(restaurant_id, group_id):
    try:
        sql = text("INSERT INTO restaurant_group (restaurant_id, group_id) VALUES (:restaurant_id, :group_id)")
        db.session.execute(sql, {"restaurant_id": restaurant_id, "group_id": group_id})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding restaurant to group: {e}")
        return False


def get_restaurant_groups(restaurant_id):
    try:
        sql = text("SELECT g.id, g.name FROM groups g JOIN restaurant_group rg ON g.id = rg.group_id WHERE rg.restaurant_id = :restaurant_id")
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        groups = result.fetchall()
        return groups
    except Exception as e:
        print(f"Error fetching restaurant groups: {e}")
        return []


def update_restaurant_groups(restaurant_id, groups):
    try:
        delete_sql = text("DELETE FROM restaurant_group WHERE restaurant_id = :restaurant_id")
        db.session.execute(delete_sql, {"restaurant_id": restaurant_id})
        for group_id in groups:
            sql = text("INSERT INTO restaurant_group (restaurant_id, group_id) VALUES (:restaurant_id, :group_id)")
            db.session.execute(sql, {"restaurant_id": restaurant_id, "group_id": group_id})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error updating restaurant groups: {e}")
        return False
    




#Arvostelu jutut
    
#Arvostelun lisääminen
def add_review(restaurant_id, user_id, review_text, rating):
    try:
        sql = text("INSERT INTO reviews (restaurant_id, user_id, review_text, rating) VALUES (:restaurant_id, :user_id, :review_text, :rating)")
        db.session.execute(sql, {"restaurant_id": restaurant_id, "user_id": user_id, "review_text": review_text, "rating": rating})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding review: {e}")
        return False
    
#Arvostelun poistaminen 
def delete_review(review_id):
    try:
        sql = text("DELETE FROM reviews WHERE id = :review_id")
        db.session.execute(sql, {"review_id": review_id})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error deleting review: {e}")
        return False
    

#Arvostelujen tulostus
def get_reviews_with_users(restaurant_id):
    try:
        sql = text("""
            SELECT r.id AS review_id, r.rating, r.review_text, r.created_at, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.restaurant_id = :restaurant_id
        """)
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        reviews = []
        for row in result:
            review = {
                'id': row[0],
                'rating': row[1],
                'review_text': row[2],
                'created_at': row[3],
                'username': row[4]
            }
            reviews.append(review)
        return reviews
    except Exception as e:
        print(f"Error fetching reviews with users: {e}")
        return []

