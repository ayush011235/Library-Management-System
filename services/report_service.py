from datetime import date
class ReportService:
  def __init__(self,db):
    self.db=db
  def get_currently_borrowed_books(self):
    query="""
    SELECT 
    t.TransactionID,
    b.Title,
    m.Name,
    t.BorrowDate,
    t.DueDate,
    t.Status
    FROM Transactions t
    INNER JOIN Books b
    ON t.BookID = b.BookID
    INNER JOIN Members m
    ON t.MemberID=m.MemberID
    WHERE t.Status = ?
    ORDER BY t.DueDate;"""
    self.db.cursor.execute(
      query,
      ('Borrowed',)
    )
    return self.db.cursor.fetchall()
  def get_most_borrowed_books(self):
    query="""
    SELECT b.Title,
    COUNT(*) AS TimesBorrowed
    FROM Transactions t
    INNER JOIN Books b
    ON t.BookID = b.BookID
    GROUP BY b.Title
    ORDER BY TimesBorrowed DESC"""
    self.db.cursor.execute(query)
    return self.db.cursor.fetchall()
  def get_overdue_books(self):
    query = """
    SELECT
    t.TransactionID,
    b.Title,
    m.Name,
    t.BorrowDate,
    t.DueDate,
    t.Status
    FROM Transactions t
    INNER JOIN Books b
    ON t.BookID = b.BookID
    INNER JOIN Members m
    ON t.MemberID=m.MemberID
    WHERE t.Status = ?
    AND t.DueDate < ?
    ORDER BY t.DueDate;"""
    self.db.cursor.execute(
      query,
      (
        "Borrowed",
        date.today()
      )
    )
    return self.db.cursor.fetchall()