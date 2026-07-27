import pyodbc
from models.member import Member 
class MemberService:
  def __init__(self,db,validator):
    self.db=db
    self.validator=validator
  def add_member(self,member):
    is_valid,message=self.validator.validate(member)

    if not is_valid:
      return False,message
    try:
      query="""INSERT INTO Members 
      (
      Name,
      Email,
      Phone,
      Address,
      JoinDate,
      IsActive
      )
      VALUES 
      (?,?,?,?,?,?)"""
      self.db.cursor.execute(query,
        (member.name,
         member.email,
         member.phone,
         member.address,
         member.join_date,
         member.is_active
        )
      )

      self.db.commit()
      return True,"Member Added Successfully."
    except pyodbc.Error as e:
      self.db.rollback()
      return False.str(e)
  def _rows_to_members(self,rows):
    members=[]
    for row in rows:
      members.append(Member.from_db_row(row))
    return members

  def get_all_members(self):
    query="""
    SELECT * FROM Members"""
    self.db.cursor.execute(query)
    rows=self.db.cursor.fetchall()
    return self._rows_to_members(rows)

  def get_member_by_id(self,member_id):
    query="""
    SELECT * FROM Members WHERE MemberID = ?"""
    self.db.cursor.execute(query,(member_id,))
    row = self.db.cursor.fetchone()
    if row is None:
      return None
    return Member.from_db_row(row)

  def search_members(self,keyword):
    keyword = f"%{keyword}%"
    query="""
    SELECT * FROM Members
    WHERE
    Name LIKE ?
    OR Email LIKE ?
    OR Phone LIKE ?"""
    self.db.cursor.execute(
      query,
      (
        keyword,
        keyword,
        keyword
      ))     
    rows = self.db.cursor.fetchall()
    return self._rows_to_members(rows)
  def update_member(self,member):
    existing_member = self.get_member_by_id(member.member_id)
    if existing_member is None:
      return False,"Member not found."
    is_valid,message=self.validator.validate(member)
    if not is_valid:
      return False,message

    try:
      query = """
      UPDATE Members
      SET 
      Name = ?,
      Email = ?,
      Phone = ?,
      Address = ?
      WHERE MemberID = ?"""

      self.db.cursor.execute(
        query,
        (
          member.name,
          member.email,
          member.phone,
          member.address,
          member.member_id
        )
      )
      self.db.commit()

      return True,"Member updated successfully."
    except pyodbc.Error as e:
      self.db.rollback()
      return False,str(e)
  def delete_member(self,member_id):
    member = self.get_member_by_id(member_id)
    if member is None:
      return False, "Member is not found."
    if not member.is_active:
      return False,"Member is already inactive."

    try:
      query="""
      UPDATE Members
      SET IsActive = 0
      WHERE MemberID = ?
      """
      self.db.cursor.execute(query,(member_id,))
      self.db.commit()

      return True,"Member deactivated successfully."
    except Exception as e:
      self.db.rollback()
      return False , str(e)

  