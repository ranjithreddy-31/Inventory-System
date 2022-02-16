use praneeth

create table userDetails (Name varchar(50), Password varchar(50), Email varchar(100));


create table customerDetails (customerID int, name varchar(50), zip int, taxRate numeric, email varchar(100));

create table invoiceDetails (id int, [Name] varchar(50), zip numeric, taxRate numeric, itemName varchar(50),sellingPrice numeric, deliveryCharges numeric, totalPrice numeric, dateOfPurchase varchar(50), isClosed int);


drop table invoiceDetails

select * from invoiceDetails
truncate table invoiceDetails
insert into invoiceDetails (id, Name, zip, taxRate, itemName,sellingPrice, deliveryCharges, totalPrice, dateOfPurchase) values (2,'Ranjith',90815,10,'TV',100,0,110.0, '02-15-2022');
insert into invoiceDetails values (2,'Ranjith',90815,10,'TV',100,0,110.0, '02-15-2022');

select * from invoiceDetails order by dateOfPurchase;

