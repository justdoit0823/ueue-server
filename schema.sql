-- MySQL dump 10.13  Distrib 5.1.71, for redhat-linux-gnu (i386)
--
-- Host: localhost    Database: ueue
-- ------------------------------------------------------
-- Server version	5.1.71-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `basicinfo`
--

DROP TABLE IF EXISTS `basicinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basicinfo` (
  `bsc_id` int(11) NOT NULL DEFAULT '0',
  `uname` char(20) DEFAULT NULL,
  `area` char(10) DEFAULT NULL,
  `organ` char(40) DEFAULT NULL,
  `job` char(40) DEFAULT NULL,
  `height` char(10) DEFAULT NULL,
  `weight` char(10) DEFAULT NULL,
  `birth` char(20) DEFAULT NULL,
  `extend` char(30) DEFAULT NULL,
  `vertext` text COMMENT '用户验证文字',
  `vercode` varchar(16) NOT NULL COMMENT '验证码',
  PRIMARY KEY (`bsc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contactinfo`
--

DROP TABLE IF EXISTS `contactinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactinfo` (
  `con_id` int(11) DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `telphone` char(20) DEFAULT NULL,
  `conmail` char(30) DEFAULT NULL,
  `conaddress` char(40) DEFAULT NULL,
  `sinawb` char(30) DEFAULT NULL,
  `qqwb` char(30) DEFAULT NULL,
  `qq` char(20) DEFAULT NULL,
  `qzone` char(30) DEFAULT NULL,
  `renren` char(30) DEFAULT NULL,
  `douban` char(30) DEFAULT NULL,
  `psldomain` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `type` char(10) DEFAULT NULL,
  `title` char(24) DEFAULT NULL,
  `content` varchar(1024) DEFAULT NULL,
  `place` char(30) DEFAULT NULL,
  `lable` char(30) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  `view` int(11) NOT NULL DEFAULT '0',
  `support` int(11) NOT NULL DEFAULT '0',
  `review` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0',
  `picture` varchar(1024) DEFAULT NULL,
  `echeck` char(1) DEFAULT NULL,
  `check_status` int(1) DEFAULT '4',
  PRIMARY KEY (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eventreview`
--

DROP TABLE IF EXISTS `eventreview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventreview` (
  `erid` int(11) NOT NULL AUTO_INCREMENT,
  `revieweid` int(11) DEFAULT NULL,
  `reviewuid` int(11) DEFAULT NULL,
  `content` char(200) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  PRIMARY KEY (`erid`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eventsupport`
--

DROP TABLE IF EXISTS `eventsupport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventsupport` (
  `esid` int(11) NOT NULL AUTO_INCREMENT,
  `supeid` int(11) DEFAULT NULL,
  `supuid` int(11) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  PRIMARY KEY (`esid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eventview`
--

DROP TABLE IF EXISTS `eventview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventview` (
  `evid` int(11) NOT NULL AUTO_INCREMENT,
  `vieweid` int(11) DEFAULT NULL,
  `viewuid` int(11) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  PRIMARY KEY (`evid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `fid` int(11) DEFAULT NULL,
  `flwid` int(11) DEFAULT NULL,
  `relation` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `muid` int(11) DEFAULT NULL,
  `mtype` char(1) DEFAULT NULL,
  `content` char(200) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property` (
  `proper_id` int(11) NOT NULL DEFAULT '0',
  `ptype` char(1) DEFAULT NULL,
  `sex` char(1) DEFAULT NULL,
  PRIMARY KEY (`proper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) DEFAULT NULL,
  `account` char(16) DEFAULT NULL,
  `email` char(30) DEFAULT NULL,
  `password` char(60) DEFAULT NULL,
  `img` char(80) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `code` char(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `work`
--

DROP TABLE IF EXISTS `work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `work` (
  `wid` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `title` char(24) DEFAULT NULL,
  `content` varchar(1024) DEFAULT NULL,
  `wdescribe` varchar(1000) DEFAULT NULL,
  `cover` char(100) DEFAULT NULL,
  `lable` char(30) DEFAULT NULL,
  `copysign` char(1) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  `view` int(11) NOT NULL DEFAULT '0',
  `support` int(11) NOT NULL DEFAULT '0',
  `review` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0',
  `wcheck` int(11) DEFAULT NULL,
  `check_status` int(1) DEFAULT '4',
  PRIMARY KEY (`wid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workreview`
--

DROP TABLE IF EXISTS `workreview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workreview` (
  `wrid` int(11) NOT NULL AUTO_INCREMENT,
  `reviewwid` int(11) DEFAULT NULL,
  `reviewuid` int(11) DEFAULT NULL,
  `content` char(200) DEFAULT NULL,
  `time` char(30) DEFAULT NULL,
  PRIMARY KEY (`wrid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-19  7:06:15
