from pydantic import BaseModel


# A schema for a base user
class UserBase(BaseModel):
    """
    Base class for all user models.
    """
    email: str


# A schema for register
class UserRegisterIn(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


# A schema for login
class UserLoginIn(UserBase):
    password: str
