from models.user import User
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
    if password != user.password_hash:
      return False,"Invalid password",None
    return True,"Login Successful.",user
