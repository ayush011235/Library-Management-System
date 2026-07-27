from models.transaction import Transaction
from datetime import date
class CirculationService:
  def __init__(self,db,book_service,member_service):
    self.db = db
    self.book_service = book_service
    self.member_service = member_service
  def _get_active_transaction(self,book_id,member_id):
    query="""SELECT * FROM Transactions WHERE BookID=? AND MemberID=? AND Status=? """
    status = 'Borrowed'
    self.db.cursor.execute(
      query,
      (
        book_id,
        member_id,
        status
      )
    )
    row = self.db.cursor.fetchone()

    if row is None:
      return None
    return Transaction.from_db_row(row)

  def borrow_book(self,book_id,member_id):
    book=self.book_service.get_book_by_id(book_id)
    if book is None:
      return False,"Book not found."

    member = self.member_service.get_member_by_id(member_id)
    if member is None:
      return False,"Member not found."

    if not member.is_active:
      return False,"Member is inactive."

    if book.available_copies <= 0:
      return False, "No copies available."

    transaction=Transaction(book_id,member_id)

    try:
      book.available_copies -= 1
      update_query = """
      UPDATE Books
      SET AvailableCopies = ?
      WHERE BookID = ?"""

      self.db.cursor.execute(
        update_query,
        (
          book.available_copies,
          book.book_id
        )
      )
      insert_query = """
      INSERT INTO Transactions
      (
      BookID,
      MemberID,
      BorrowDate,
      DueDate,
      ReturnDate,
      Status
      )
      VALUES
      (?,?,?,?,?,?)"""
      self.db.cursor.execute(
        insert_query,
        (
          transaction.book_id,
          transaction.member_id,
          transaction.borrow_date,
          transaction.due_date,
          transaction.return_date,
          transaction.status
        )
      )
      self.db.commit()

      return True, "Book borrowed successfully"
    except Exception as e:
      self.db.rollback()
      return False,str(e)

  def return_book(self,book_id,member_id):
    transaction = self._get_active_transaction(book_id,member_id)
    if transaction is None:
      return False,"This member has not borrowed this book."
    book = self.book_service.get_book_by_id(book_id)

    if book is None:
      return False,"Book not found."
    try:
      book.available_copies += 1
      transaction.return_date= date.today()
      transaction.status="Returned"
      update_book_query = """
      UPDATE Books
      SET AvailableCopies = ?
      WHERE BookID=?"""
      self.db.cursor.execute(
        update_book_query,
        (
          book.available_copies,
          book.book_id
        )
      )      
      update_transaction_query = """
      UPDATE Transactions
      SET
        ReturnDate = ?,
        Status = ?
        WHERE TransactionID = ?"""
      self.db.cursor.execute(
        update_transaction_query,
        (
          transaction.return_date,
          transaction.status,
          transaction.transaction_id
        )
      )

      self.db.commit()
      return True, "Book returned successfully."
    except Exception as e:
      self.db.rollback()
      return False,str(e)
