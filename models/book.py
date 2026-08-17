class Book:
  def __init__(self,title,author,category,isbn,total_copies,book_id=None):
    self.book_id=book_id
    self.title=title
    self.author=author
    self.category=category
    self.isbn=isbn
    self.total_copies=total_copies
    self.available_copies=total_copies
  def __str__(self):
    return (
      f"\nBook ID          : {self.book_id}"
      f"\nTitle            : {self.title}"
      f"\nAuthor           : {self.author}"
      f"\nCategory         : {self.category}"
      f"\nISBN             : {self.isbn}"
      f"\nTotal Copies     : {self.total_copies}"
      f"\nAvailable Copies : {self.available_copies}"
  )
  @classmethod
  def from_db_row(cls,row): # here cls is representing the class itself
    book=cls(
      title=row.Title,
      author=row.Author,
      category=row.Category,
      isbn=row.ISBN,
      total_copies=row.TotalCopies,
      book_id=row.BookID
    )
    book.available_copies=row.AvailableCopies
    return book


