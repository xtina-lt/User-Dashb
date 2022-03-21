from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from datetime import datetime
import math

class Message:
    db = "user_dash"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.reciever = User.select_one({"id" : data["reciever_id"]})
        self.sender = User.select_one({"id" : data["sender_id"]})
        self.created_at = Message.time_passed(data["created_at"])
        self.updated_at = Message.time_passed(data["updated_at"])
    
    @staticmethod
    def time_passed(e):
        now = datetime.now()
        delta = now - e
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
    
    @classmethod
    def create(cls, data):
        query="INSERT INTO messages(content, sender_id, reciever_id) VALUES(%(content)s, %(sender)s, %(reciever)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def read_recieved(cls, data):
        query="SELECT * FROM messages WHERE reciever_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(i) for i in results]
    
    @classmethod
    def read_sent(cls, data):
        query="SELECT * FROM messages WHERE sender_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(i) for i in results]
    
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM messages WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def edit(cls, data):
        query="UPDATE messages SET content=%(content)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query="DELETE FROM messages WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)