from app import db

class Articles(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    article_id = db.Column(db.String(20), unique = True, nullable = False)
    topic = db.Column(db.String(20), unique = False, nullable = True)
    abstract = db.Column(db.String(500), unique = False, nullable = True)
    link = db.Column(db.String(200), unique = False, nullable = True)
    date = db.Column(db.DateTime)
    
    def __repr__(self):
        
        return f"id : {self.id}\n topic : {self.topic}\n abstract : {self.abstract}\n date : {self.date}\n"