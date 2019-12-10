create database allbestbets;
use allbestbets;

create table login(
login nvarchar(30),
pass nvarchar(50),
proxy nvarchar(50)
);

create table work_parser(
date_work datetime,
status_work nvarchar(50),
status tinyint);

create table vilki(
percent decimal(14, 10) signed,
min_koef decimal(20, 10) signed,
max_koef decimal(20, 10) signed,
initiator int,
event_name nvarchar(500),
team1_name nvarchar(300),
team2_name nvarchar(300),
league nvarchar(300),
sport_id int unsigned,
country_id int unsigned);

create user 'scrapper'@'%' identified by '123456';
grant all privileges on *.* to 'scrapper'@'%';
flush privileges;
