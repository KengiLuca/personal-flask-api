from application import db, app

app.app_context().push()

class StarwarsCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    catch_phrase = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name, type, catch_phrase):
        self.name = name
        self.type = type
        self.catch_phrase = catch_phrase
    
    def __repr__(self):
        return f"My name is {self.name} and my catch phrase is {self.catch_phrase}"
