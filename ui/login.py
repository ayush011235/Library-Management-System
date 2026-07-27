class LoginUI:
  def __init__(self,auth_service):
    self.auth_service=auth_service

  def login(self):
    while True:
      print("="*40)
      print(" LIBRARY LOGIN ")
      print("="*40)

      username = input("Username:")
      password = input("Password:")

      success,message,user=self.auth_service.login(
        username,password
      )
      print(message)
      if success:
        return user
    
    