drop database if exists AIdriven ;
create database AIdriven ;
use AIdriven ;

create table users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(225),
    email VARCHAR(50), 
    password VARCHAR(50)
    );
