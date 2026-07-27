import pyodbc

class DatabaseConnection:
  def __init__(self):
    self.connection=None
    self.cursor=None
    self.connect()

  def connect(self):
    try:
      self.connection=pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-49FUPK8\\SQLEXPRESS;"
        "DATABASE=LibraryDB;"
        "Trusted_Connection=yes;"
      )
      self.cursor = self.connection.cursor()
      print("Database Connected Successfully")
    except pyodbc.Error as e:
      print("Connection Error:",e)
  def commit(self):
    self.connection.commit()
  def rollback(self):
    self.connection.rollback()
  def close(self):
    if self.cursor:
      self.cursor.close()
    if self.connection:
      self.connection.close()

    print("Database Connection closed")
