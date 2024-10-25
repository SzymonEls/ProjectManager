from app.extensions import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.String(255))
    path = db.Column(db.String(255), unique=True)
    url = db.Column(db.Boolean, server_default="0", nullable=False)


    def __repr__(self):
        return f'<File "{self.title}">'