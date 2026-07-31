use LibraryDB;
create table Admin(
AdminID int primary key identity(1,1),
Username varchar(50) not null unique,
password varchar(255) not null,
);


create table Books(
BookID int identity(1,1) primary key,
Title varchar(200) not null,
Author varchar(100) not null,
Category varchar(100),
ISBN varchar(20) unique,
TotalCopies int not null check(TotalCopies >=0), -- A check constraint validates the data before it's stored.
AvailableCopies int not null check(AvailableCopies >= 0),--A column level check constraint
constraint CHK_AvailableCopies check(AvailableCopies <= TotalCopies),-- table level constraint
);

create table Members(
MemberID int identity(1,1) primary key,
Name varchar(100) not null,
Phone varchar(15),
Email varchar(100),
Address varchar(200),
JoinDate Date not null,
IsActive Bit not null Default 1,
);

create table Transactions(
TransactionID int identity(1,1) primary key,
BookID int not null,
MemberID int not null,
BorrowDate Date not null Default getDate(),
DueDate date not null,
ReturnDate Date null,
Status varchar(20) not null,
foreign key (BookID) references Books(BookID),
foreign key (MemberID) references Members(MemberID),
);
use LibraryDB;
select * from Books;
select * from Members;

select * from Transactions;
update Books 
set AvailableCopies = 0
where BookID = 1;

update Transactions 
set DueDate = '2026-07-20'
where TransactionID = 4;

create table Users(
UserID int identity(1,1) primary key,
Username varchar(255) not null unique,
PasswordHash varchar(255) not null,
FullName varchar(100) not null,
Role varchar(20) not null,
IsActive bit not null default 1
);

insert into Users
(
Username,
PasswordHash,
FullName,
Role
)
values
(
'admin',
'admin123',
'System Administrator',
'Admin'
);

select * from Users;
delete from Users where Username='admin';
insert into Users
(
	Username,
	PasswordHash,
	FullName,
	Role,
	IsActive
)
values
(
	'admin',
	'$2b$12$B6/aRgtlWnyhRKdAE8ZkM.McWR13aCXVQXRg/ZDc33ehkcLZ2oGna',
	'System Administrator',
	'Admin',
	1
);

insert into Users
(
	Username,
	PasswordHash,
	FullName,
	Role,
	IsActive
)
values
(
	'librarian',
	'$2b$12$h.SZYkZG9Z7FqfMsqVZclewV3UjcYZVz/rr0Hdqr968fweedaZGhW',
	'Librayr Staff',
	'Librarian',
	1
);

	