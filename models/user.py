from uuid import uuid4
import bcrypt
from sqlalchemy import Column, Integer, String, LargeBinary
from models.basemodel import Base, BaseModel
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    """
    User account model
    """
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    password = Column(LargeBinary, nullable=False)
    
    def __init__(self, **data):
        super().__init__(**data)
        if 'password' in data:
            self.password = self.hash_password(data['password'])

    def hash_password(self, password):
        """Hash the password before saving it"""
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    
    def check_password(self, password):
        """Check the password during login"""
        return bcrypt.checkpw(password.encode('utf8'), self.password)
