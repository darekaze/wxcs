"""Model handling file."""
from datetime import datetime

from wxcs import db


class UserLog(db.Model):
    """The user log model."""

    id = db.Column(db.Integer, primary_key=True)
    dtg = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(20), nullable=False)
    post = db.Column(db.String(20), nullable=False)
    wxid = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Print userlog detail."""
        return f'UserLog("{self.dtg}", "{self.name}", "{self.post}", "{self.wxid}", "{self.role}")'
