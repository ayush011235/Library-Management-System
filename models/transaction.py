from datetime import date,timedelta

class Transaction:
  def __init__(self,book_id,member_id,transaction_id=None):
    self.transaction_id = transaction_id
    self.book_id= book_id
    self.member_id=member_id
    self.borrow_date=date.today()
    self.due_date=self.borrow_date+timedelta(days=14)
    self.return_date = None
    self.status="Borrowed"

  def __str__(self):
    return (
      f"Transaction ID                : {self.transaction_id}\n"
      f"Book ID                       : {self.book_id}\n"
      f"Member ID                     : {self.member_id}\n"
      f"Borrow Date                   : {self.borrow_date}\n"
      f"Due Date                      : {self.due_date}\n"
      f"Return Date                   : {self.return_date}\n"
      f"Status                        : {self.status}"
      f"\nFine                        : {self.calculate_fine()}"
    )
  @classmethod
  def from_db_row(cls,row):
    transaction=cls(
      row.BookID,
      row.MemberID,
      row.TransactionID
    )
    transaction.borrow_date = row.BorrowDate
    transaction.due_date = row.DueDate
    transaction.status = row.Status
    return transaction

 
  
    
    