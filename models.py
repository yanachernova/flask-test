from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user = db.Column(db.String(50), nullable=False)
    '''for view the contacts whit a define format'''
    def __repr__(self):
        return '<Todo %r>' % self.label    
    
    '''for view the contacts whit a define format'''
    def serialize(self):
        return{
            'id':self.id,
            'label':self.label,
            'done':self.done,
            'user':self.user
        }