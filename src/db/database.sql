drop database if exists bjg1dstrxqky2rlrd5aa;
create database bjg1dstrxqky2rlrd5aa;
use bjg1dstrxqky2rlrd5aa;
create table users(
	id int unsigned auto_increment primary key,
    nombre varchar(50),
    apellido varchar(50),
    ciudad varchar(50),
    pais varchar(50)
)