"""Model handling file."""
from sqlalchemy.orm import relationship, backref
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
    wxid = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Display userlog detail."""
        return f'UserLog("{self.created_at}", "{self.name}", "{self.post}", "{self.wxid}", "{self.role}")'


class Case(db.Model):
    """The case model."""

    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(60), nullable=True)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    log = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)

    links = relationship('Link', secondary='toolsets')
    logs = relationship('UserLog', backref='user', lazy=True)

    def __repr__(self):
        """Display userlog detail."""
        return f'Case("{self.codename}", "{self.title}", "{self.start_at}", "{self.end_at}", "{self.log}")'


class Link(db.Model):
    """The Link model.

    ctg - Category No.
        0 = Uncategorized
        1 = Observations
        2 = Prognoses
        3 = Operations
        4 = Others
    """

    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    href = db.Column(db.String(80), nullable=False)
    icon = db.Column(db.String(80), nullable=True)
    ctg = db.Column(db.Integer, nullable=True)
    interval_min = db.Column(db.Integer, nullable=True)
    base_min = db.Column(db.Integer, nullable=True)
    post = db.Column(db.String(20), nullable=True)

    cases = relationship('Case', secondary='toolsets')

    def __repr__(self):
        """Display userlog detail."""
        return f'Link("{self.name}", "{self.href}", "{self.post}")'


class Toolset(db.Model):
    """Model for showing tools used in cases."""

    __tablename__ = 'toolsets'

    codename = db.Column(db.String(20), db.ForeignKey('cases.codename'), primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), primary_key=True)

    case = relationship(Case, backref=backref('toolsets', cascade='all, delete-orphan'))
    link = relationship(Link, backref=backref('toolsets', cascade='all, delete-orphan'))

    def __repr__(self):
        """Display userlog detail."""
        return f'Toolset("{self.wxid}", "{self.linkid}")'


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
        return f'Admin("{self.username}")'
