if not exists (select * from userDetails where Name='Testuser' )
insert into userDetails values ('Testuser', 'sample', 'samplemail@csulb.edu');