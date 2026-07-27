class User:
  def __init__(self,username,password_hash,full_name,role,is_active=True,user_id=None):
    self.user_id = user_id
    self.username = username
    self.password_hash=password_hash
    self.full_name=full_name
    self.role = role
    self.is_active=is_active

  @classmethod
  def from_db_record(cls,row):
    return cls(
      user_id = row.UserID,
      username = row.Username,
      password_hash = row.PasswordHash,
      full_name=row.FullName,
      role=row.Role,
      is_active = row.IsActive
    )
  def __str__(self):
    return (
      f"User ID :{self.user_id}\n"
      f"Username : {self.username}\n"
      f"Full Name : {self.full_name}\n"
      f"Role : {self.role}\n"
      f"Active : {self.is_active}"
    )
    