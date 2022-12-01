create database ctf2;
use ctf2;

create table users (
	user char(20) not null unique,
	pass char(50) not null,
	salt char(30) not null,
	primary key (user)
) ENGINE=InnoDB;

create table transfers (
	id mediumint not null auto_increment, 
	user char(20) not null, 
	amount int not null default 0, 
	tstamp datetime not null default CURRENT_TIMESTAMP, 
	foreign key(user) references users(user), 
	primary key (id),
	check(amount>=0)
) ENGINE=InnoDB;


insert into users values('jelena','42scb7b112aa98218c4a9a8d29cd6b51610aabde10f9','848d258371');
insert into users values('john','42scb7b112aada847b51846d4c94f18ae6a934eb7b1d','55b7e84c6a');
insert into users values('kate','42scb7b112aadeac98ae1cfda55521005afd026bf8e1','ac2bbbe79b');
insert into transfers (user, amount, tstamp) values ('jelena','100', now());
insert into transfers (user, amount, tstamp) values ('john','100', now());
insert into transfers (user, amount, tstamp) values ('kate','300', now());


CREATE USER 'script@localhost' IDENTIFIED BY 'ude2z&YU3Mq!LR#!%h#e';
GRANT SELECT, INSERT ON ctf2.users to 'script@localhost';
GRANT SELECT, INSERT ON ctf2.transfers to 'script@localhost';
