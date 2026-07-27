from datetime import date

class Member:
  def __init__(self,name,email,phone,address,member_id=None,join_date=None,is_active=True):
    self.member_id=member_id
    self.name=name
    self.email=email
    self.phone=phone
    self.address=address
    self.join_date= join_date if join_date else date.today()
    self.is_active=is_active

  def __str__(self):
    return (
          f"\nMember ID       : {self.member_id}"
          f"\nName            : {self.name}"
          f"\nEmail           : {self.email}"
          f"\nPhone           : {self.phone}"
          f"\nAddress         : {self.address}"
          f"\nJoin Date       : {self.join_date}"
          f"\nStatus          : {self.is_active}"
      )
  @classmethod
  def from_db_row(cls,row):
    """Creates a Member object from database row."""
    member=cls(
      name=row.Name,
      email=row.Email,
      phone=row.Phone,
      address=row.Address,
      member_id=row.MemberID,
      join_date=row.JoinDate,
      is_active=row.IsActive
    )
    return member