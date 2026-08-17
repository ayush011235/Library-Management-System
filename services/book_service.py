import pyodbc
from models.book import Book
class BookService:
  def __init__(self,db,validator):
    self.db=db
    self.validator=validator
  def _rows_to_books(self,rows):# private helper method:-method is intended for internal use with a leading underscore
    books=[]
    for row in rows:
      books.append(Book.from_db_row(row))
    return books
  def add_book(self,book):
    is_valid,message=self.validator.validate(book)
    if not is_valid:
      return False,message
    try:
      query="""INSERT INTO Books 
      (Title,
      Author,
      Category,
      ISBN,
      TotalCopies,
      AvailableCopies)
      VALUES 
      (?,?,?,?,?,?)"""
      self.db.cursor.execute(query,
        (book.title,
        book.author,
        book.category,
        book.isbn,
        book.total_copies,
        book.available_copies
        )
      )
      self.db.commit()
      return True,"Book Added Successfully."
    except pyodbc.Error as e:
      return False.str(e)      
  def get_all_books(self):
    query="""SELECT * FROM Books"""
    self.db.cursor.execute(query)
    rows=self.db.cursor.fetchall()
    return self._rows_to_books(rows)
  def get_book_by_id(self,book_id):
    query="""SELECT * FROM Books WHERE BookID=?"""
    self.db.cursor.execute(query,(book_id,))
    row=self.db.cursor.fetchone()
    if row is None:
      return None
    else:
      return Book.from_db_row(row)
  def search_books(self,keyword):
    query="""SELECT * FROM Books
    WHERE
     Title LIKE ?
     OR Author LIKE ?
     OR Category LIKE ?
     OR ISBN LIKE ?"""
    self.db.cursor.execute(query,
      (
      f"%{keyword}%",
      f"%{keyword}%",
      f"%{keyword}%",
      f"%{keyword}%"
      )
    )
    rows=self.db.cursor.fetchall()
    return self._rows_to_books(rows)
  def update_book(self,updated_book):
    existing_book=self.get_book_by_id(updated_book.book_id)
    if existing_book is None:
      return False,"Book not found."
    is_valid,message=self.validator.validate(updated_book)
    if not is_valid:
      return False,message
    issued_books=(existing_book.total_copies-existing_book.available_copies)
    new_available = updated_book.total_copies-issued_books
    if new_available < 0:
      return (False,"Total copies cannot be less than issued books.")
    try:
      query="""UPDATE Books
      SET
      Title=?,
      Author=?,
      Category=?,
      ISBN=?,
      TotalCopies=?,
      AvailableCopies=?
      WHERE BookID=?"""
      self.db.cursor.execute(
        query,
        (
          updated_book.title,
          updated_book.author,
          updated_book.category,
          updated_book.isbn,
          updated_book.total_copies,
          new_available,
          updated_book.book_id
        )
      )
      self.db.commit()
      return True,"Book Updated Successfully."
    except pyodbc.Error as e:
      self.db.rollback()
      return False,str(e)
  def delete_book(self,book_id):
    existing_book=self.get_book_by_id(book_id)
    if existing_book is None:
      return False,"Book not found."
    issued_books=(
      existing_book.total_copies - existing_book.available_copies
    )
    if issued_books > 0:
      return False,"Cannot delete a book that has issued copies"
    query="""DELETE FROM Books WHERE BookID=?"""
    self.db.cursor.execute(query,(book_id,))
    self.db.commit()
    return True,"Book has been delete successfully."

