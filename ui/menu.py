from models.book import Book
from models.member import Member
from datetime import date
class Menu:
  def __init__(self,book_service,member_service,circulation_service,report_service):
    self.book_service=book_service
    self.member_service=member_service
    self.circulation_service=circulation_service
    self.report_service=report_service
  def report_menu(self):
    while True:
      print("\n=============REPORT MENU =============")
      print("1. Currently Borrowed Books")
      print("2. Overdue Books")
      print("3. Back")
      choice = input("Enter Your choice:")
      if choice == "1":
        self.view_currently_borrowed_books()
      elif choice == '2':
        self.view_overdue_books()
      elif choice == '3':
        break
      else:
        print("Invalid Choice")
  def show_menu(self):
    print("\n"+"+"*40)
    print("     LIBRARY MANAGEMENT SYSTEM")
    print("="*40)
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Books")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Add Member")
    print("7. View Members")
    print("8. Search Member")
    print("9. Update Member")
    print("10. Delete Member")
    print("11. Borrow Book")
    print("12.Return Book")
    print("13. Reports")
    print("0. Exit")
    print("="*40)

  def start(self,current_user):
    print(f"\nWelcome {current_user.full_name}")
    print(f"Role:{current_user.role}")
    while True:
      self.show_menu()
      choice=input("Enter your choice:")
      if choice == "1":
        self.add_book()
      elif choice == "2":
        self.view_books()
      elif choice == "3":
        self.search_books()
      elif choice == "4":
        self.update_book()
      elif choice == "5":
        self.delete_book()
      elif choice == "6":
        self.add_member()
      elif choice == "7":
        self.view_members()
      elif choice == "8":
        self.search_members()
      elif choice == "9":
        self.update_member()
      elif choice == "10":
        self.delete_member()
      elif choice == "11":
        self.borrow_book()
      elif choice == "12":
        self.return_book()
      elif choice == "13":
        self.report_menu()
      elif choice == "0":
        print("\nThank you for using Library Management System.")
        break
      else:
        print("Invalid choice! Please try again.")
  def add_book(self):
    print("\n--------Add New Book---------")
    title=input("Enter Title:")
    author=input("Enter Author:")
    category=input("Enter Category:")
    isbn=input("Enter ISBN:")
    total=int(input("Enter Total Copies:"))
  
    book=Book(title,author,category,isbn,total)
    success,message=self.book_service.add_book(book)
    print(message)
  def view_books(self):
    print("\n----------All Books------------")
    books=self.book_service.get_all_books()
    if not books:
      print("No books available.")
      return
    for book in books:
      print(book)
      print("-"*40)
  def search_books(self):
    keyword=input("Enter the keyword by which you want to find the book:")
    books=self.book_service.search_books(keyword)
    if not books:
      print("No books found.")
      return
    print("\nSearch Results\n")
    for book in books:
      print(book)
      print('-'*40)
  def update_book(self):
    print("\n---------Update Book----------")
    book_id=int(input("Enter the id of the book you want to update:"))
    book=self.book_service.get_book_by_id(book_id)
    if book:
      print("Current Book")
      print(book)
  
      book.title=input("New Title:")
      book.author=input("New Author:")
      book.category=input("New Category:")
      book.isbn=input("New ISBN:")
      book.total_copies=int(input("New Total Copies:"))
      success,message=self.book_service.update_book(book)
      print(message)
    else:
      print("book not found")
  def delete_book(self):
    print("\n----------Delete Book-----------")
    book_id=int(input("Enter the id of the book You want to delete:"))
    success,message=self.book_service.delete_book(book_id)
    print(message)

  def add_member(self):
    print("\n-----------Add New Member------------")
    name = input("Enter Name: ")
    email = input("Enter Emial: ")
    phone = input("Enter Phone: ")
    address= input("Enter Address: ")

    member = Member(
      name,
      email,
      phone,
      address
    )
    success,message=self.member_service.add_member(member)
    print(message)

  def view_members(self):
    print("\n----------All Members------------")
    members=self.member_service.get_all_members()

    if not members:
      print("No members found.")
      return
    for member in members:
      print(member)
      print("-"*50)
  def search_members(self):
    keyword = input("Enter keyword:")
    members = self.member_service.search_members(keyword)
    if not members:
      print("No members found.")
      return
    for member in members:
      print(member)
      print("-"*50)

  def update_member(self):
    member_id = int(input("Enter Member ID:"))
    member = self.member_service.get_member_by_id(member_id)
    if member is None:
      print("Member not found.")
      return
    member.name = input(f"Name ({member.name}):") or member.name
    member.email = input(f"Email ({member.email}):") or member.email
    member.phone = input(f"Phone ({member.phone}):") or member.phone
    member.address = input(f"Address ({member.address}):") or member.address

    success,message=self.member_service.update_member(member)
    print(message)

  def delete_member(self):
    member_id = int(input("Enter Member ID:"))
    success,message=self.member_service.delete_member(member_id)
    print(message)
    
    # db.close()

  def borrow_book(self):
    try:
      book_id = int(input("Enter Book ID:"))
      member_id = int(input("Enter Member ID:"))
      success,message=self.circulation_service.borrow_book(book_id,member_id)
      print(message)

    except ValueError:
      print("Please Enter valid numeric IDs.")
  def return_book(self):
    try:
      book_id=int(input("Enter Book ID : "))
      member_id=int(input("Enter Member ID :"))
      success,message=self.circulation_service.return_book(book_id,member_id)
      print(message)
    except ValueError:
      print("Please enter valid numeric IDs.")

  def view_currently_borrowed_books(self):
    rows=self.report_service.get_currently_borrowed_books()

    if not rows:
      print("\nNo books are currently borrowed.")
      return
    print("\nCurrent Borrowed Books")
    print("-"*90)
    print(f"{'Txn ID':<8}{'Book':<30}{'Member':<20}{'Borrowe Date':<15}{'Due Date'}")
    print("-"*90)

    for row in rows:
      print(
        f"{row.TransactionID:<8}"
        f"{row.Title:<30}"
        f"{row.Name:<20}"
        f"{str(row.BorrowDate):<15}"
        f"{str(row.DueDate)}"
      )
  def view_overdue_books(self):
    rows = self.report_service.get_overdue_books()
    if not rows:
      print("\nNo Overdue books")
      return
    print("\nOVERDUE BOOKS")
    print("-"*120)
    print(
      f"{'Txn ID':<8}"
      f"{'Book':<30}"
      f"{'Member':<20}"
      f"{'Due Date':<15}"
      f"{'Days':<8}"
      f"{'Fine'}"
    )
    print('-'*120)
    for row in rows:
      days = (date.today()-
      row.DueDate).days
      fine=days*10
      print(
        f"{row.TransactionID:<8}"
        f"{row.Title:<30}"
        f"{row.Name:<20}"
        f"{str(row.DueDate):<15}"
        f"{days:<8}"
        f"Rs{fine}"              
      )
  

    