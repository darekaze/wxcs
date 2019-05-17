"""Model handling file."""
from datetime import datetime
from flask_login import UserMixin
from wxcs import bcrypt, db, login_manager


@login_manager.user_loader
def load_admin(admin_id):
    """Load admin info by id."""
    return Admin.query.get(int(admin_id))


class UserLog(db.Model):
    """The user log model."""

    __tablename__ = 'userlogs'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(20), nullable=False)
    post = db.Column(db.String(20), nullable=False)
    wxid = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Display userlog detail."""
        return f'UserLog("{self.dtg}", "{self.name}", "{self.post}", "{self.wxid}", "{self.role}")'


class Admin(db.Model, UserMixin):
    """The admin model."""

    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Return admin detail."""
        return f"Admin('{self.username}')"
