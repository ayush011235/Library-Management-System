class BookValidator:
  # @staticmethod # we can call it without creating object of BookValidator
  def validate(self,book):
    if not book.title.strip():
      return False,'Book Title cannot be empty'
    elif not book.author.strip():
      return False,'Book Author cannot be empty'
    elif not book.isbn.strip():
      return False,'Book isbn cannot be empty'
    elif book.total_copies <= 0:
      return False,'Total copies must be greater than 0'
    else:
      return True,None

class MemberValidator:
  def validate(self,member):
    if not member.name.strip():
      return False,"Name Cannot be empty."
    if not member.email.strip():
      return False,"Email cannot be empty."
    if not member.phone.strip():
      return False,"Phone cannot be empty."
    if not member.address.strip():
      return False,"Address cannot be empty."
    return True,None

class UserValidator:
  @staticmethod
  def validate(username,password):
    if not username.strip():
      return False,"Username cannot be empty."
    elif not password.strip():
      return False,"Password cannot be empty."
    return True,None
  @staticmethod
  def validate_user(user):
    if not user.username.strip():
      return False,"Username cannot be empty."
    if not user.password_hash.strip():
      return False,"Password cannot be empty."
    if len(user.password_hash)<6:
      return False,"Password must be at least 6 characters."
    if not user.full_name.strip():
      return False,"Full name cannot be empty."
    if user.role not in ("Admin","Librarian"):
      return False,"Invalid role."
    return True,None