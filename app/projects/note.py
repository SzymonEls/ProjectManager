from app.extensions import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Project "{self.title}">'