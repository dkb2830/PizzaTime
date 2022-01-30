# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Order:
    db = 'pizza_petes'
    def __init__( self , data ):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.quantity = data['quantity']
        self.toppings = ''
        self.created_at = ''
        self.updated_at = ''
        self.order_total = float(0)
        # Now we use class methods to query our database
    
    @classmethod
    def save_order(cls, data ):
        query = "INSERT INTO orders ( method, size, crust, quantity, toppings, user_id ) VALUES ( %(method)s , %(size)s, %(crust)s, %(quantity)s, %(toppings)s %(user_id)s );"
    
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def delete_order(cls, data ):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        
        return connectToMySQL(cls.db).query_db(query, data)
