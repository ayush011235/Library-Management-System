from models.user import User
import bcrypt
from utils.validators import UserValidator
class AuthenticationService:
  def __init__(self,db):
    self.db = db 
    self.validator = UserValidator()
  def login(self,username,password):
    is_valid,message=self.validator.validate(username,password)
    if not is_valid:
      return False,message,None
    query="""
    SELECT * FROM Users WHERE Username = ?"""
    self.db.cursor.execute(query,(username,))
    row=self.db.cursor.fetchone()
    if row is None:
      return False,"Invalid username",None
    user=User.from_db_record(row)
    if not user.is_active:
      return False,"Account is inactive.",None
    if not bcrypt.checkpw(
      password.encode(),
      user.password_hash.encode()
    ):
      return False,"Invalid password",None
    return True,"Login Successful.",user
  def add_user(self,user):
    is_valid,message=self.validator.validate_user(user)
    if not is_valid:
      return False,message
    query="""
    SELECT UserID
    FROM Users
    WHERE Username = ?"""
    self.db.cursor.execute(query,(user.username,))
    if self.db.cursor.fetchone():
      return False,"Username already exists."
    password_hash = bcrypt.hashpw(
      user.password_hash.encode(),
      bcrypt.gensalt()
    ).decode()
    query="""
    INSERT INTO Users
    (
      Username,
      PasswordHash,
      FullName,
      Role,
      IsActive
    )
    VALUES
    (
      ?,?,?,?,?
    )"""
    self.db.cursor.execute(
      query,
      (
        user.username,
        password_hash,
        user.full_name,
        user.role,
        user.is_active
      )
    )
    self.db.connection.commit()
    return True,"User added successfully."