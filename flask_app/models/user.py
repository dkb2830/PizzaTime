# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order import Order

class User:
    db = 'pizza_petes'
    def __init__( self , data ):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.favorite_order = ''
        self.created_at = ''
        self.updated_at = ''
    # Now we use class methods to query our database
        self.orders = []
        
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        
        print(results[0])
        return cls(results[0])
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstname , lastname , email, password, address, city, state) VALUES ( %(fname)s , %(lname)s , %(email)s, %(password)s, %(address)s, %(city)s, %(state)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        
        if len(results) < 1:
            return False
        
        return cls(results[0])
    
    @classmethod
    def get_orders_by_user(cls, data):
        query = "SELECT orders.* FROM orders WHERE orders.user_id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_user_favorite(cls, data):
        query = "UPDATE users SET favorite = %(favorite)s WHERE id %(id)s;"
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_favorite_order(cls, data):
        query = "SELECT orders.* FROM orders WHERE orders.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        
        return Order(results[0])