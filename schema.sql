-- Copyright 2009 FriendFeed
--
-- Licensed under the Apache License, Version 2.0 (the "License"); you may
-- not use this file except in compliance with the License. You may obtain
-- a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--


-- youyizuobiao database
--
-- This is a struction of youyizuobiao database,add what need to this
--

-- To create the database:
--   CREATE DATABASE shareyou;
--   GRANT ALL PRIVILEGES ON yoez.* TO 'root'@'localhost' IDENTIFIED BY 'yoez';
--
-- To reload the tables:
--   mysql --user=root --password=**** --database=yoez < schema.sql


SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";


DROP TABLE IF EXISTS user;
CREATE TABLE user(
    uid INT primary key,
    account CHAR(8),
    email CHAR(30),
    password char(60),
    img char(80),
    time char(30),
    status int not null default 0,
    code char(36)
);

DROP TABLE IF EXISTS event;
CREATE TABLE event(
    eid int auto_increment primary key,
    author_id int,
    type char(1),
    title char(24),
    content varchar(1024),
    place char(30),
    picture varchar(1024),
    lable char(30),
    time char(30),
    view int not null default 0,
    support int not null default 0,
    review int not null default 0,
    status char(1) not null default 0
);

DROP TABLE IF EXISTS eventview;
CREATE TABLE eventview(
    evid int auto_increment primary key,
    vieweid int,
    viewuid int,
    time char(30)
);

DROP TABLE IF EXISTS eventsupport;
CREATE TABLE eventsupport(
    esid int auto_increment primary key,
    supeid int,
    supuid int,
    time char(30)
);

DROP TABLE IF EXISTS eventreview;
CREATE TABLE eventreview(
    erid int auto_increment primary key,
    revieweid int,
    reviewuid int,
    content char(140),
    time char(30)
);

DROP TABLE IF EXISTS work;
CREATE TABLE work(
    wid int auto_increment primary key,
    author_id int,
    type char(1),
    title char(24),
    content varchar(1024),
    wdescribe varchar(1000),
    cover char(100),
    lable char(30),
    copysign char(1),
    time char(30),
    teammates char(100),
    view int not null default 0,
    support int not null default 0,
    review int not null default 0,
    status char(1) not null default 0
);

DROP TABLE IF EXISTS workreview;
CREATE TABLE workreview(
    wrid int auto_increment primary key,
    reviewwid int,
    reviewuid int,
    content char(140),
    time char(30)
);

DROP TABLE IF EXISTS property;
CREATE TABLE property(
    proper_id int primary key,
    ptype char(1),
    sex char(1),
    content char(255)
);

DROP TABLE IF EXISTS contactinfo;
CREATE TABLE contactinfo(
    con_id int primary key,
    agent_id int,
    telphone char(20),
    conmail char(30),
    conaddress char(40),
    sinawb char(30),
    qqwb char(30),
    qq char(20),
    qzone char(30),
    renren char(30),
    douban char(30),
    psldomain char(30)
);

DROP TABLE IF EXISTS basicinfo;
CREATE TABLE basicinfo(
    bsc_id int primary key,
    uname char(20),
    area char(10),
    organ char(40),
    job char(40),
    height char(10),
    weight char(10),
    birth char(20),
    extend char(30)
);

DROP TABLE IF EXISTS follow;
CREATE TABLE follow(
    fid int,
    flwid int,
    relation char(1)
);

DROP TABLE IF EXISTS message;
CREATE TABLE message(
    mid int auto_increment primary key,
    muid int,
    mtype char(1),
    content char(200),
    time char(30)
);