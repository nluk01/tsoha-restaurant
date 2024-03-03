from sqlalchemy import text
from db import db
import users


# Lisää uusi ravintola
def add_restaurant(name, opening_hours, description, location, groups):
    try:
        sql = text("INSERT INTO restaurants (name, opening_hours, description, location) VALUES (:name, :opening_hours, :description, :location) RETURNING id")
        result = db.session.execute(sql, {"name": name,"opening_hours":opening_hours, "description": description, "location": location})
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
def update_restaurant(restaurant_id, name,  opening_hours, description, location,groups):
    try:
        sql = text("UPDATE restaurants SET name=:name, opening_hours=:opening_hours, description=:description, location=:location WHERE id=:id")
        db.session.execute(sql, {"name": name, "opening_hours":opening_hours, "description": description, "location": location, "id": restaurant_id})
        if update_restaurant_groups(restaurant_id, groups):
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating restaurant: {e}")
        return False
    

# Hae ravintolan valitut ryhmät
def get_groups_for_restaurant(restaurant_id):
    try:
        sql = text("SELECT group_id FROM restaurant_group WHERE restaurant_id = :restaurant_id")
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        groups = [row[0] for row in result]
        return groups
    except Exception as e:
        print(f"Error fetching groups for restaurant: {e}")
        return []



# Ravintolan tulostushommat
def get_restaurant_by_id(restaurant_id):
    try:
        sql = text("SELECT id, name, opening_hours, description, location FROM restaurants WHERE id = :id")
        result = db.session.execute(sql, {"id": restaurant_id})
        restaurant = result.fetchone()
        return restaurant
    except Exception as e:
        print(f"Error fetching restaurant: {e}")
        return None


#Haetaan tietokannasta kaikki ravintoloiden tiedot  
def get_all_restaurants():
    try:
        sql = text("""
            SELECT r.id, r.name, r.opening_hours, r.description, r.location, ARRAY_AGG(g.name) AS groups
            FROM restaurants r
            LEFT JOIN restaurant_group rg ON r.id = rg.restaurant_id
            LEFT JOIN groups g ON rg.group_id = g.id
            GROUP BY r.id, r.name, r.opening_hours, r.description, r.location
        """)
        result = db.session.execute(sql)
        restaurants = []
        for row in result:
            restaurant = {
                'id': row[0],
                'name': row[1],
                'opening_hours': row[2],
                'description': row[3],
                'location': row[4],
                'groups': row[5] if row[5] else []  
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

#Päivitä ravintolan tiedot muokkauksen jälkeen
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
def delete_review(review_id, user_id=None):
    try:
        if user_id and not users.admin(user_id):
            sql = text("DELETE FROM reviews WHERE id = :review_id AND user_id = :user_id")
            db.session.execute(sql, {"review_id": review_id, "user_id": user_id})
        else:
            sql = text("DELETE FROM reviews WHERE id = :review_id")
            db.session.execute(sql, {"review_id": review_id})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error deleting review: {e}")
        return False



# Arvostelun tulostus
def get_reviews_with_users(restaurant_id):
    try:
        sql = text("SELECT reviews.id, reviews.restaurant_id, reviews.user_id, reviews.review_text, reviews.rating, reviews.created_at, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE restaurant_id = :restaurant_id")
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        reviews = []
        for row in result:
            review = {
                'id': row[0],
                'restaurant_id': row[1],
                'user_id': row[2],
                'review_text': row[3],
                'rating': row[4],
                'created_at': row[5],
                'username': row[6]
            }
            reviews.append(review)
        return reviews
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []
    


#Sanan hakeminen ravintoloiden kuvauksesta
    
def get_restaurants_by_description(search_term):
    try:
        sql = text("""
            SELECT id, name,opening_hours, description, location
            FROM restaurants
            WHERE LOWER(description) LIKE LOWER(:search_term)
        """)
        result = db.session.execute(sql, {"search_term": f"%{search_term}%"})
        restaurants = result.fetchall()
        return restaurants
    except Exception as e:
        print(f"Error fetching restaurants by description: {e}")
        return []


#Parhaat raflat
def get_restaurants_by_rating():
    try:
        sql = text("""
            SELECT 
                r.id, 
                r.name, 
                r.opening_hours, 
                r.description, 
                r.location, 
                ROUND(AVG(reviews.rating), 1) AS average_rating
            FROM 
                restaurants r
            LEFT JOIN 
                reviews ON r.id = reviews.restaurant_id
            GROUP BY 
                r.id
            HAVING 
                COUNT(reviews.rating) > 0 -- Suodatetaan pois arvostelut, joissa ei ole annettu arvosanaa
            ORDER BY 
                average_rating DESC NULLS LAST
        """)
        result = db.session.execute(sql)
        restaurants = []
        for row in result:
            restaurant = {
                'id': row[0],
                'name': row[1],
                'opening_hours': row[2],
                'description': row[3],
                'location': row[4],
                'average_rating': row[5]
            }
            restaurants.append(restaurant)
        return restaurants
    except Exception as e:
        print(f"Error fetching restaurants by rating: {e}")
        return []