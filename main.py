from database import DatabaseConnection
from services.book_service import BookService
from utils.validators import BookValidator,MemberValidator
from services.member_service import MemberService
from services.report_service import ReportService
from services.authentication_service import AuthenticationService
from services.circulation_service import CirculationService
from ui.menu import Menu
from ui.login import LoginUI
def main():
  db=DatabaseConnection()
  validator=BookValidator()
  book_service=BookService(db,BookValidator())
  member_service=MemberService(db,MemberValidator())
  auth_service=AuthenticationService(db)
  circulation_service = CirculationService(db,book_service,member_service)
  report_service=ReportService(db)
  # FIRST TIME SETUP
  if not auth_service.has_users():
    success=auth_service.create_first_admin()
    if not success:
      print("\nAdmin account could not be created.")
      db.close()
      return
    print("\nFirst Admin account created successfully.")
    print("Please login using your new credentials.\n")
  # NORMAL LOGIN
  login_ui=LoginUI(auth_service)
  current_user = login_ui.login()
  # MAIN MENU
  menu=Menu(book_service,member_service,circulation_service,report_service,current_user,auth_service)
  menu.start()
  db.close()

  
if __name__ == "__main__":
  main()