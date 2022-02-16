use praneeth

create table userDetails (Name varchar(50), Password varchar(50), Email varchar(100));

create table customerDetails (customerID int, name varchar(50), zip int, taxRate numeric, email varchar(100));

create table invoiceDetails (id int, Name varchar(50), zip int, email varchar(100), taxRate numeric, itemName varchar(50),sellingPrice numeric, deliveryCharges numeric, totalPrice numeric);

insert into customerDetails values(1,'Ranjith', 90815, 10,'no-email@gmail.com');

insert into invoiceDetails values(1,'Ranjith', 90815, 10,'no-email@gmail.com');