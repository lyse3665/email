from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:

    DB = "email_schema"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
       

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
        
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def is_valid_user(user_info):
        is_valid = True
        # query = "SELECT * FROM users WHERE email = %(email)s;"
        # result = connectToMySQL(cls.DB).query_db(query, user)
        if len(user_info['first_name']) <= 0:
            flash('First name required.')
            is_valid = False
        if len(user_info['last_name']) <= 0:
            flash('Last name required.')
            is_valid = False
        if len(user_info['email']) <= 0:
            flash('Email required.')
            is_valid = False
        if not EMAIL_REGEX.match(user_info["email"]):
            flash("Invalid Email!!!!","register")
            is_valid = False
        print('Validation -User is valid:', is_valid)
        return is_valid
     

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query  = """
        DELETE FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
