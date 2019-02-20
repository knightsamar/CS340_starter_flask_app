-- MySQL dump 10.16  Distrib 10.1.35-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bsg2
-- ------------------------------------------------------
-- Server version	10.1.35-MariaDB

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
-- Table structure for table `bsg_cert`
--

DROP TABLE IF EXISTS `bsg_cert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bsg_cert` (
  `certification_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`certification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_cert`
--

LOCK TABLES `bsg_cert` WRITE;
/*!40000 ALTER TABLE `bsg_cert` DISABLE KEYS */;
INSERT INTO `bsg_cert` VALUES (1,'Raptor'),(2,'Viper'),(3,'Mechanic'),(4,'Command');
/*!40000 ALTER TABLE `bsg_cert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_cert_people`
--

DROP TABLE IF EXISTS `bsg_cert_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bsg_cert_people` (
  `cid` int(11) NOT NULL DEFAULT '0',
  `pid` int(11) NOT NULL DEFAULT '0',
  `certification_date` date NOT NULL,
  PRIMARY KEY (`cid`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `bsg_cert_people_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `bsg_cert` (`certification_id`),
  CONSTRAINT `bsg_cert_people_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `bsg_people` (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_cert_people`
--

LOCK TABLES `bsg_cert_people` WRITE;
/*!40000 ALTER TABLE `bsg_cert_people` DISABLE KEYS */;
INSERT INTO `bsg_cert_people` VALUES (1,1,'0000-00-00'),(1,2,'0000-00-00'),(2,1,'0000-00-00'),(2,2,'0000-00-00'),(3,1,'0000-00-00'),(3,6,'0000-00-00'),(4,1,'0000-00-00'),(4,6,'0000-00-00');
/*!40000 ALTER TABLE `bsg_cert_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_people`
--

DROP TABLE IF EXISTS `bsg_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bsg_people` (
  `character_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(255) NOT NULL,
  `lname` varchar(255) DEFAULT NULL,
  `homeworld` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `race` varchar(5) NOT NULL DEFAULT 'Human',
  PRIMARY KEY (`character_id`),
  KEY `homeworld` (`homeworld`),
  CONSTRAINT `bsg_people_ibfk_1` FOREIGN KEY (`homeworld`) REFERENCES `bsg_planets` (`planet_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_people`
--

LOCK TABLES `bsg_people` WRITE;
/*!40000 ALTER TABLE `bsg_people` DISABLE KEYS */;
INSERT INTO `bsg_people` VALUES (1,'Will','Adama',20,634,'Human'),(2,'Lee','Adama',3,100,'Human'),(3,'Laura','Roslin',22,100,'Human'),(6,'Saul','Tigh',NULL,71,'Human'),(9,'Callandra','Henderson',NULL,NULL,'Human'),(17,'Trey','Hoover',16,23,'Human'),(18,'Luke','Bob',16,24,'Human'),(20,'Bob','Jones',2,27,'Human');
/*!40000 ALTER TABLE `bsg_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_planets`
--

DROP TABLE IF EXISTS `bsg_planets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bsg_planets` (
  `planet_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `population` bigint(20) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `capital` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`planet_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_planets`
--

LOCK TABLES `bsg_planets` WRITE;
/*!40000 ALTER TABLE `bsg_planets` DISABLE KEYS */;
INSERT INTO `bsg_planets` VALUES (1,'Gemenon',2800000000,'Old Gemenese','Oranu'),(2,'Leonis',2600000000,'Leonese','Luminere'),(3,'Caprica',4900000000,'Caprican','Caprica City'),(7,'Sagittaron',1700000000,NULL,'Tawa'),(16,'Aquaria',25000,NULL,NULL),(17,'Canceron',6700000000,NULL,'Hades'),(18,'Libran',2100000,NULL,NULL),(19,'Picon',1400000000,NULL,'Queestown'),(20,'Scorpia',450000000,NULL,'Celeste'),(21,'Tauron',2500000000,'Tauron','Hypatia'),(22,'Virgon',4300000000,NULL,'Boskirk');
/*!40000 ALTER TABLE `bsg_planets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsg_spaceship`
--

DROP TABLE IF EXISTS `bsg_spaceship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bsg_spaceship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `seperate_saucer_section` bit(1) DEFAULT b'0',
  `length` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsg_spaceship`
--

LOCK TABLES `bsg_spaceship` WRITE;
/*!40000 ALTER TABLE `bsg_spaceship` DISABLE KEYS */;
INSERT INTO `bsg_spaceship` VALUES (1,'t1','',0),(2,'t2','',0),(3,'t2','',0),(4,'t3','',0),(5,'t4','\0',0),(6,'t5','',0);
/*!40000 ALTER TABLE `bsg_spaceship` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-28 13:23:54
