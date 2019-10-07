from alayatodo import db

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('Users', backref='users')

    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean)

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'description': self.description,
                'completed': self.completed}
