CREATE DATABASE xyzbookstore;

USE xyzbookstore;

CREATE TABLE book_stock(
	UID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    book_name TEXT NOT NULL,
    book_desc TEXT NOT NULL,
    author_info TEXT,
    stock INT
);

insert into book_stock(book_name,book_desc,author_info,stock) values ('Book 1','Volume 1','Author 1, Author 2',5);
insert into book_stock(book_name,book_desc,author_info,stock) values ('Book 2','Volume 1','Author 3, Author 4',6);
insert into book_stock(book_name,book_desc,author_info,stock) values ('Book 3','Volume 1','Author 5, Author 6',7);

create table membership(
	id int auto_increment not null primary key,
    mname text not null,
    email text not null,
    duration int
);

insert into membership(mname,email,duration) values ('memb1','mem1@gmail.com',6);
insert into membership(mname,email,duration) values ('a','a@gmail.com',6);


create table bill(
	id int auto_increment not null primary key,
    books text not null,
    price text not null
);

INSERT INTO bill(books,price) VALUES('book1,book2','100,200');
INSERT INTO bill(books,price) VALUES('book1,book3','100,300');
INSERT INTO bill(books,price) VALUES('book2,book3','200,300');

commit;