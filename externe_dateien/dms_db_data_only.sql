SET NAMES utf8;

-- MySQL dump 10.11
--
-- Host: localhost    Database: dms_db
-- ------------------------------------------------------
-- Server version	5.0.45

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_dms`
--

DROP TABLE IF EXISTS `auth_group_dms`;
CREATE TABLE `auth_group_dms` (
  `id` int(11) NOT NULL auto_increment,
  `org_id` int(11) NOT NULL,
  `name` varchar(30) collate utf8_unicode_ci NOT NULL,
  `description` varchar(120) collate utf8_unicode_ci default NULL,
  `is_primary` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_group_dms_org_id` (`org_id`),
  KEY `auth_group_dms_group_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_group_dms`
--

LOCK TABLES `auth_group_dms` WRITE;
/*!40000 ALTER TABLE `auth_group_dms` DISABLE KEYS */;
INSERT INTO `auth_group_dms` VALUES (1,-1,'leiter','Leiter/in',1),(2,-1,'leitung','Leitung',1),(3,-1,'mitarbeiter','Mitarbeiter/innen',1),(4,-1,'sekretariat','Sekretariat',1),(5,-1,'assistenz','Assistenzkr&auml;fte',1);
/*!40000 ALTER TABLE `auth_group_dms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_org`
--

DROP TABLE IF EXISTS `auth_org`;
CREATE TABLE `auth_org` (
  `id` int(11) NOT NULL auto_increment,
  `org_id` int(11) NOT NULL,
  `organisation` varchar(120) collate utf8_unicode_ci NOT NULL,
  `sub_organisation` varchar(80) collate utf8_unicode_ci NOT NULL,
  `street` varchar(50) collate utf8_unicode_ci NOT NULL,
  `zip` varchar(10) collate utf8_unicode_ci NOT NULL,
  `town` varchar(50) collate utf8_unicode_ci NOT NULL,
  `phone` varchar(40) collate utf8_unicode_ci NOT NULL,
  `fax` varchar(40) collate utf8_unicode_ci NOT NULL,
  `email` varchar(200) collate utf8_unicode_ci NOT NULL,
  `homepage` varchar(200) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `org_id` (`org_id`),
  KEY `auth_org_organisation` (`organisation`),
  KEY `auth_org_town` (`town`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_org`
--

LOCK TABLES `auth_org` WRITE;
/*!40000 ALTER TABLE `auth_org` DISABLE KEYS */;
INSERT INTO `auth_org` VALUES (1,-1,'Ein p&auml;dagogisches Institut','','Torweg 1-3','12345','Neustadt','0123 / 456789','0123 / 456789','','');
/*!40000 ALTER TABLE `auth_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_org_group`
--

DROP TABLE IF EXISTS `auth_org_group`;
CREATE TABLE `auth_org_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) collate utf8_unicode_ci NOT NULL,
  `contains` varchar(40) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_org_group_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_org_group`
--

LOCK TABLES `auth_org_group` WRITE;
/*!40000 ALTER TABLE `auth_org_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_org_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) collate utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_role`
--

DROP TABLE IF EXISTS `auth_role`;
CREATE TABLE `auth_role` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(30) collate utf8_unicode_ci NOT NULL,
  `description` varchar(80) collate utf8_unicode_ci NOT NULL,
  `perm_read` tinyint(1) NOT NULL,
  `perm_add` tinyint(1) NOT NULL,
  `perm_add_folderish` tinyint(1) NOT NULL,
  `perm_edit` tinyint(1) NOT NULL,
  `perm_edit_own` tinyint(1) NOT NULL,
  `perm_edit_folderish` tinyint(1) NOT NULL,
  `perm_manage` tinyint(1) NOT NULL,
  `perm_manage_own` tinyint(1) NOT NULL,
  `perm_manage_folderish` tinyint(1) NOT NULL,
  `perm_manage_site` tinyint(1) NOT NULL,
  `perm_manage_user` tinyint(1) NOT NULL,
  `perm_manage_user_new` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2001 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_role`
--

LOCK TABLES `auth_role` WRITE;
/*!40000 ALTER TABLE `auth_role` DISABLE KEYS */;
INSERT INTO `auth_role` VALUES (10,'the_manager','Systemverwalter/in',1,1,1,1,1,1,1,1,1,1,1,1),(20,'top_manager','Verwalter/in f&uuml;r Inhalte und User (inkl. neuer User)',1,1,1,1,1,1,1,1,1,0,1,1),(30,'manager','Verwalter/in f&uuml;r Inhalte und User',1,1,1,1,1,1,1,1,1,0,1,0),(40,'co_manager','Verwalter/in f&uuml;r Inhalte',1,1,1,1,1,1,1,1,1,0,0,0),(50,'worker','Teilnehmer/in - lesend und schreibend',1,1,0,0,1,0,0,1,0,0,0,0),(60,'worker_reader','Teilnehmer/in - lesend',1,0,0,0,0,0,0,0,0,0,0,0),(70,'worker_writer','Teilnehmer/in - schreibend (f&uuml;r Pr&uuml;fungsarbeiten)',0,1,0,0,0,0,0,0,0,0,0,0),(1000,'no_rights','Ohne Rechte',0,0,0,0,0,0,0,0,0,0,0,0),(2000,'anonymous','Anonymer Zugang',0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `auth_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_sub_org`
--

DROP TABLE IF EXISTS `auth_sub_org`;
CREATE TABLE `auth_sub_org` (
  `id` int(11) NOT NULL auto_increment,
  `org_id` int(11) NOT NULL,
  `name` varchar(30) collate utf8_unicode_ci NOT NULL,
  `description` varchar(80) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_sub_org_org_id` (`org_id`),
  KEY `auth_sub_org_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_sub_org`
--

LOCK TABLES `auth_sub_org` WRITE;
/*!40000 ALTER TABLE `auth_sub_org` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_sub_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(60) collate utf8_unicode_ci NOT NULL,
  `sex` varchar(10) collate utf8_unicode_ci NOT NULL,
  `title` varchar(30) collate utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) collate utf8_unicode_ci NOT NULL,
  `last_name` varchar(40) character set utf8 NOT NULL,
  `email` varchar(75) collate utf8_unicode_ci NOT NULL,
  `password` varchar(80) collate utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL default '0',
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','m','','','Admin','admin@demo.org','{SSHA}Mkk1ixfuTaFg/1cEGPb5WTwsAQUGeQ8ocmH2',1,1,1,'2007-11-27 14:04:44','2007-11-27 14:04:44');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_group`
--

DROP TABLE IF EXISTS `auth_user_group`;
CREATE TABLE `auth_user_group` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_user_group_user_id` (`user_id`),
  KEY `auth_user_group_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_user_group`
--

LOCK TABLES `auth_user_group` WRITE;
/*!40000 ALTER TABLE `auth_user_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_org`
--

DROP TABLE IF EXISTS `auth_user_org`;
CREATE TABLE `auth_user_org` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `org_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_user_org_user_id` (`user_id`),
  KEY `auth_user_org_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_user_org`
--

LOCK TABLES `auth_user_org` WRITE;
/*!40000 ALTER TABLE `auth_user_org` DISABLE KEYS */;
INSERT INTO `auth_user_org` VALUES (1,1,-1);
/*!40000 ALTER TABLE `auth_user_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_url_role`
--

DROP TABLE IF EXISTS `auth_user_url_role`;
CREATE TABLE `auth_user_url_role` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `container_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_user_url_role_user_id` (`user_id`),
  KEY `auth_user_url_role_folder_id` (`container_id`),
  KEY `auth_user_url_role_role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_user_url_role`
--

LOCK TABLES `auth_user_url_role` WRITE;
/*!40000 ALTER TABLE `auth_user_url_role` DISABLE KEYS */;
INSERT INTO `auth_user_url_role` VALUES (1,1,1,10);
/*!40000 ALTER TABLE `auth_user_url_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cache_tb`
--

DROP TABLE IF EXISTS `cache_tb`;
CREATE TABLE `cache_tb` (
  `cache_key` varchar(255) collate utf8_unicode_ci NOT NULL,
  `value` longtext collate utf8_unicode_ci NOT NULL,
  `expires` datetime NOT NULL,
  PRIMARY KEY  (`cache_key`),
  UNIQUE KEY `cache_key` (`cache_key`),
  KEY `cache_tb_expires` (`expires`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `cache_tb`
--

LOCK TABLES `cache_tb` WRITE;
/*!40000 ALTER TABLE `cache_tb` DISABLE KEYS */;
/*!40000 ALTER TABLE `cache_tb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext collate utf8_unicode_ci,
  `object_repr` varchar(200) collate utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) collate utf8_unicode_ci NOT NULL,
  `app_label` varchar(100) collate utf8_unicode_ci NOT NULL,
  `model` varchar(100) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'message','auth','message'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'permission','auth','permission'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(16,'dms_css','css','dms_css'),(27,'dms item','dms','dmsitem'),(29,'dms site','dms','dmssite'),(30,'dms app','dms','dmsapp'),(31,'dms user org','dms','dmsuserorg'),(39,'dms container','dms','dmscontainer'),(40,'dms user url role','dms','dmsuserurlrole'),(41,'dms roles','dms','dmsroles'),(42,'dms org','dms','dmsorg'),(43,'dms sub org','dms','dmssuborg'),(45,'dms user group','dms','dmsusergroup'),(46,'dms group','dms','dmsgroup'),(47,'dms comment','dms','dmscomment'),(51,'dms download protected','dms','dmsdownloadprotected'),(52,'dms feed','dms','dmsfeed'),(54,'dms feed item','dms','dmsfeeditem'),(55,'dms item container','dms','dmsitemcontainer'),(56,'dms app allowed','dms','dmsappallowed'),(59,'dms media survey','mediasurvey','dmsmediasurvey'),(60,'dms media survey_items','mediasurvey','dmsmediasurvey_items'),(61,'dms media survey_gruppe','mediasurvey','dmsmediasurvey_gruppe'),(64,'dms media survey_gruppe_form','mediasurvey','dmsmediasurvey_gruppe_form'),(66,'dms media survey_option','mediasurvey','dmsmediasurvey_option'),(67,'dms anti spam','dms','dmsantispam'),(68,'dms search engine','dms','dmssearchengine'),(69,'dms license','dms','dmslicense'),(70,'dms nav menu left','dms','dmsnavmenuleft'),(71,'dms nav menu top','dms','dmsnavmenutop'),(73,'fort_ fach','fortbildung','fort_fach'),(74,'fort_ schulart','fortbildung','fort_schulart'),(75,'dms org group','dms','dmsorggroup'),(77,'dms edu lern res typ','edufolder','dmsedulernrestyp'),(78,'dms edu medienformat','edufolder','dmsedumedienformat'),(79,'dms edu fach sachgebiet','edufolder','dmsedufachsachgebiet'),(80,'dms edu zielgruppe','edufolder','dmseduzielgruppe'),(81,'dms edu schulstufe','edufolder','dmseduschulstufe'),(82,'dms edu schulart','edufolder','dmseduschulart'),(83,'dms elixier org','elixier','dmselixierorg'),(84,'dms elixier item','elixier','dmselixieritem'),(85,'dms elixier quelle','elixier','dmselixierquelle'),(86,'dms elixier medienformat','elixier','dmselixiermedienformat'),(87,'dms elixier schlagwort','elixier','dmselixierschlagwort'),(88,'dms elixier fach','elixier','dmselixierfach'),(89,'dms elixier bildungsebene','elixier','dmselixierbildungsebene'),(90,'dms edu objekt','edufolder','dmseduobjekt'),(92,'dms edu zertifikat','edufolder','dmseduzertifikat'),(93,'dms edu item','edufolder','dmseduitem'),(94,'dms edu sprache','edufolder','dmsedusprache'),(95,'dms edu schlagwort','edufolder','dmseduschlagwort'),(96,'dms edu org','edufolder','dmseduorg'),(97,'dms edu schlagwort stem','edufolder','dmseduschlagwortstem');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) collate utf8_unicode_ci NOT NULL,
  `session_data` longtext collate utf8_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ca24444875bdd8fb314ef1e587bd4783','gAJ9cQEuYzBkMDFiZjMwZGUyY2JiMjk0MmRiNTg3Y2JkMGUxY2Y=\n','2007-12-12 16:14:52');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) collate utf8_unicode_ci NOT NULL,
  `name` varchar(50) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com'),(2,'http://dms.bildung.de','Bildungsserver XYZ');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item`
--

DROP TABLE IF EXISTS `dms_dms_edu_item`;
CREATE TABLE `dms_dms_edu_item` (
  `id` int(11) NOT NULL auto_increment,
  `item_id` int(11) NOT NULL,
  `metadaten_url` varchar(200) NOT NULL,
  `autor` varchar(120) NOT NULL,
  `herausgeber` varchar(250) NOT NULL,
  `anbieter_herkunft` varchar(250) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `preis` varchar(20) NOT NULL,
  `titel_lang` longtext NOT NULL,
  `beschreibung_lang` longtext NOT NULL,
  `publikations_datum` varchar(30) default NULL,
  `standards_kmk` longtext NOT NULL,
  `standards_weitere` longtext NOT NULL,
  `techn_voraus` longtext NOT NULL,
  `lernziel` longtext NOT NULL,
  `lernzeit` varchar(20) NOT NULL,
  `methodik` longtext NOT NULL,
  `lehrplan` longtext NOT NULL,
  `rechte` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dms_edu_item_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item`
--

LOCK TABLES `dms_dms_edu_item` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_fach_sachgebiet`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_fach_sachgebiet`;
CREATE TABLE `dms_dms_edu_item_fach_sachgebiet` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmsedufachsachgebiet_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmsedufachsachgebiet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_fach_sachgebiet`
--

LOCK TABLES `dms_dms_edu_item_fach_sachgebiet` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_fach_sachgebiet` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_fach_sachgebiet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_schlagwort`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_schlagwort`;
CREATE TABLE `dms_dms_edu_item_schlagwort` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmseduschlagwort_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmseduschlagwort_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_schlagwort`
--

LOCK TABLES `dms_dms_edu_item_schlagwort` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_schlagwort` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_schlagwort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_schulart`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_schulart`;
CREATE TABLE `dms_dms_edu_item_schulart` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmseduschulart_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmseduschulart_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_schulart`
--

LOCK TABLES `dms_dms_edu_item_schulart` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_schulart` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_schulart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_schulstufe`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_schulstufe`;
CREATE TABLE `dms_dms_edu_item_schulstufe` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmseduschulstufe_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmseduschulstufe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_schulstufe`
--

LOCK TABLES `dms_dms_edu_item_schulstufe` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_schulstufe` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_schulstufe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_sprache`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_sprache`;
CREATE TABLE `dms_dms_edu_item_sprache` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmsedusprache_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmsedusprache_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_sprache`
--

LOCK TABLES `dms_dms_edu_item_sprache` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_sprache` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_sprache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_item_zielgruppe`
--

DROP TABLE IF EXISTS `dms_dms_edu_item_zielgruppe`;
CREATE TABLE `dms_dms_edu_item_zielgruppe` (
  `id` int(11) NOT NULL auto_increment,
  `dmseduitem_id` int(11) NOT NULL,
  `dmseduzielgruppe_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `dmseduitem_id` (`dmseduitem_id`,`dmseduzielgruppe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_item_zielgruppe`
--

LOCK TABLES `dms_dms_edu_item_zielgruppe` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_item_zielgruppe` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dms_edu_item_zielgruppe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dms_edu_org`
--

DROP TABLE IF EXISTS `dms_dms_edu_org`;
CREATE TABLE `dms_dms_edu_org` (
  `id` int(11) NOT NULL auto_increment,
  `schluessel` varchar(20) NOT NULL,
  `beschreibung` varchar(120) NOT NULL,
  `url` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dms_edu_org_schluessel` (`schluessel`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dms_edu_org`
--

LOCK TABLES `dms_dms_edu_org` WRITE;
/*!40000 ALTER TABLE `dms_dms_edu_org` DISABLE KEYS */;
INSERT INTO `dms_dms_edu_org` VALUES (1,'HE','Bildungsserver Hessen','http://www.bildung.hessen.de/'),(2,'NDS','Nieders&auml;chsischer Bildungsserver','http://www.nibis.de/'),(3,'SODIS','Sodis','http://www.sodis.de/'),(4,'DBS','Deutscher Bildungsserver','http://www.bildungsserver.de/'),(5,'LPO.HE','Lehrplan online (Hessen)','http://www.lpo-hessen.de/'),(6,'LBS-BW','Landesbildungsserver Baden-WÃ¼rtemberg','http://lbsneu.schule-bw.de/'),(7,'SN','Landesbildungsserver Sachsen','http://www.sn.schule.de/');
/*!40000 ALTER TABLE `dms_dms_edu_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsantispam`
--

DROP TABLE IF EXISTS `dms_dmsantispam`;
CREATE TABLE `dms_dmsantispam` (
  `id` int(11) NOT NULL auto_increment,
  `question` varchar(120) NOT NULL,
  `answer` varchar(20) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsantispam`
--

LOCK TABLES `dms_dmsantispam` WRITE;
/*!40000 ALTER TABLE `dms_dmsantispam` DISABLE KEYS */;
INSERT INTO `dms_dmsantispam` VALUES (1,'Wie hei&szlig;t die Hauptstadt von Deutschland?','berlin'),(2,'Wie hei&szlig;t die Hauptstadt von Italien?','rom'),(3,'Wie hei&szlig;t die Hauptstadt von Frankreich?','paris'),(4,'Wie hei&szlig;t die Hauptstadt von Gro&szlig;britannien?','london'),(5,'Wie hei&szlig;t die Hauptstadt von Spanien?','madrid'),(6,'Welcher Himmelsk&ouml;rper dreht sich um die Erde?','mond'),(7,'Um welchen Himmelsk&ouml;rper dreht sich die Erde?','sonne'),(8,'Was ist der Gegensatz zu \'hell\'?','dunkel'),(9,'Welcher Fluss flie&szlig;t durch Frankfurt? ','main');
/*!40000 ALTER TABLE `dms_dmsantispam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsapp`
--

DROP TABLE IF EXISTS `dms_dmsapp`;
CREATE TABLE `dms_dmsapp` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(40) collate utf8_unicode_ci NOT NULL,
  `description` varchar(60) collate utf8_unicode_ci NOT NULL,
  `is_folderish` tinyint(1) NOT NULL,
  `is_userfolder` tinyint(1) NOT NULL,
  `is_linkable` tinyint(1) NOT NULL,
  `is_available` tinyint(1) NOT NULL default '1',
  `has_own_breadcrumb` tinyint(1) NOT NULL,
  `sub_app_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmsapp`
--

LOCK TABLES `dms_dmsapp` WRITE;
/*!40000 ALTER TABLE `dms_dmsapp` DISABLE KEYS */;
INSERT INTO `dms_dmsapp` VALUES (1,'dmsFolder','Ordner',1,0,0,1,0,0),(2,'dmsDocument','Informationsseite',0,0,1,1,0,0),(3,'dmsUserFolder','Community-Mitglieder verwalten',1,1,0,1,0,0),(4,'dmsRedirect','Weiterleitung auf eine andere Web-Adresse',0,0,1,1,0,0),(5,'dmsLecture','Vortrag',1,0,0,1,1,0),(6,'dmsSheet','Folie eines Vortrags',0,0,0,1,0,5),(7,'dmsGuestbook','G&auml;stebuch',1,0,0,1,0,0),(8,'dmsGuestbookItem','G&auml;stebuchbeitrag',0,0,0,1,0,7),(9,'dmsUserManagement','User-Verwaltung',0,0,0,1,0,0),(10,'dmsSoftlink','Einblendung (Soft-Link)',0,0,0,1,0,0),(11,'dmsFile','Datei (PDF, Word, Excel ...)',0,0,1,1,0,0),(12,'dmsNewsboard','Nachrichtenbrett',1,0,0,1,0,0),(13,'dmsNewsItem','Nachricht',0,0,1,1,0,12),(14,'dmsImage','Bilder, Fotos, Grafiken',0,0,1,1,0,0),(15,'dmsImagethumb','Minibild',0,0,1,1,0,0),(16,'dmsRssFeedManager','RSS-Feeds',0,0,0,1,0,0),(17,'dmsPool','Materialpool',1,0,0,1,0,0),(18,'dmsMediaSurvey','Medien-Fragebogen',0,0,0,1,0,0),(19,'dmsLinklist','Link-Liste',1,0,0,1,0,0),(20,'dmsLinkItem','Verweis in Linkliste',0,0,1,1,0,19),(21,'dmsSearchXapian','Suchinterface f&uuml;r Xapian-Volltextsuche',0,0,0,1,0,0),(22,'dmsText','Textseite',0,0,1,1,0,0),(23,'dmsEventboard','Infotafel (f&uuml;r l&auml;nger andauernde Ereignisse, Veran',1,0,0,1,0,0),(24,'dmsEventItem','Termin f&uuml;r Infotafel',0,0,1,1,0,0),(25,'dmsEduFolder','Online-Lernarchiv',1,0,1,1,0,0),(26,'dmsProjectgroup','Geschlossene Arbeitsgruppe',1,0,0,1,1,0),(27,'dmsUserChangeManagement','Personendaten &auml;ndern',0,0,0,1,0,0),(28,'dmsUserRegistration','Registrierung der Community-Mitglieder',0,0,0,1,0,0),(29,'dmsRssFeed','RSS-Feed',0,0,0,1,0,0),(30,'dmsEduLinkItem','Verweis in Online-Lernarchiven',0,0,1,1,0,25),(31,'dmsDiscussboard','Diskussionsforum',1,0,0,1,0,0),(32,'dmsDiscussItem','Diskussionsbeitrag',0,0,0,1,0,31),(33,'dmsPinboard','Pinnwand',1,0,0,1,0,0),(34,'dmsPinItem','Beitrag f&uuml;r Pinnwand',0,0,0,1,0,33),(37,'dmsElixier','Elixier-Austauschdatenbank',0,0,0,1,0,0),(38,'dmsEduTextItem','Textseite in Online-Lernarchiven',0,0,1,1,0,25),(39,'dmsEduFileItem','Datei in Online-Lernarchiven',0,0,1,1,0,25),(40,'dmsEduMediaItem','Medienpaket in Online-Lernarchiven',1,0,1,1,0,25),(41,'dmsEduWebquestItem','Webquests in Online-Lernarchiven',1,0,1,1,1,25),(42,'dmsFAQboard','FAQ-Liste',1,0,0,1,0,0),(43,'dmsFAQItem','FAQ-Beitrag',0,0,1,1,0,42),(44,'dmsGallery','Galerie',1,0,0,1,0,0),(45,'dmsPhoto','Fotos f&uuml;r Galerie',0,0,1,1,0,0),(46,'dmsEduGalleryItem','Galerie in Online-Lernarchiven',1,0,1,1,0,0),(47,'dmsToDoList','To-Do-LIste',1,0,0,1,0,0),(48,'dmsToDoItem','Auftrag f&uuml;r To-Do-Liste',0,0,0,1,0,47),(49,'dmsEmailForm','Formular zum Versenden von E-Mails',0,0,0,1,0,0),(50,'dmsNewsletter','Newsletter',1,0,0,1,0,0),(51,'dmsNewsletterItem','Beitrag zu einem Newsletter',0,0,1,1,0,0),(52,'dmsFolderProtected','Gesch&uuml;tzter Ordner',1,0,0,1,0,0);
/*!40000 ALTER TABLE `dms_dmsapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsappallowed`
--

DROP TABLE IF EXISTS `dms_dmsappallowed`;
CREATE TABLE `dms_dmsappallowed` (
  `id` int(11) NOT NULL auto_increment,
  `parent_app_id` int(11) NOT NULL,
  `child_app` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsappallowed_parent_app_id` (`parent_app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsappallowed`
--

LOCK TABLES `dms_dmsappallowed` WRITE;
/*!40000 ALTER TABLE `dms_dmsappallowed` DISABLE KEYS */;
INSERT INTO `dms_dmsappallowed` VALUES (1,3,-1),(2,5,6),(3,5,11),(4,5,14),(5,7,8),(6,12,13),(7,12,12),(8,16,-1),(9,17,2),(10,17,4),(11,17,11),(12,17,14),(13,17,20),(14,17,22),(15,17,30),(16,17,38),(17,17,39);
/*!40000 ALTER TABLE `dms_dmsappallowed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmscomment`
--

DROP TABLE IF EXISTS `dms_dmscomment`;
CREATE TABLE `dms_dmscomment` (
  `id` int(11) NOT NULL auto_increment,
  `parent_item_id` int(11) NOT NULL,
  `name` varchar(80) collate utf8_unicode_ci NOT NULL,
  `email` varchar(200) collate utf8_unicode_ci default NULL,
  `title` varchar(80) collate utf8_unicode_ci NOT NULL,
  `text` longtext collate utf8_unicode_ci,
  `value` int(11) NOT NULL,
  `is_browseable` tinyint(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmscomment_parent_id` (`parent_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmscomment`
--

LOCK TABLES `dms_dmscomment` WRITE;
/*!40000 ALTER TABLE `dms_dmscomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmscomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmscontainer`
--

DROP TABLE IF EXISTS `dms_dmscontainer`;
CREATE TABLE `dms_dmscontainer` (
  `id` int(11) NOT NULL auto_increment,
  `this_item_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  `path` varchar(240) collate utf8_unicode_ci NOT NULL,
  `is_top_folder` tinyint(1) NOT NULL,
  `min_role_id` int(11) NOT NULL default '-1',
  `nav_title` varchar(60) collate utf8_unicode_ci NOT NULL,
  `menu_top_id` bigint(11) NOT NULL default '1',
  `menu_left_id` bigint(11) NOT NULL default '1',
  `nav_name_top` varchar(60) collate utf8_unicode_ci NOT NULL,
  `nav_name_left` varchar(60) collate utf8_unicode_ci NOT NULL,
  `sections` longtext collate utf8_unicode_ci NOT NULL,
  `show_next` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `path` (`path`),
  KEY `dms_dmsdirectory_parent_id` (`this_item_id`),
  KEY `dms_dmsdirectory_site_id` (`site_id`),
  KEY `menu_top_id` (`menu_top_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmscontainer`
--

LOCK TABLES `dms_dmscontainer` WRITE;
/*!40000 ALTER TABLE `dms_dmscontainer` DISABLE KEYS */;
INSERT INTO `dms_dmscontainer` VALUES (1,1,1,'/',0,2000,'Bildungsserver',1,1,'|','|','Aktuell\r\nUnterportale\r\n',0),(2,3,1,'/schwerpunkte/',0,2000,'Aktuelle Schwerpunkte',1,1,'|','dms|','Bereiche\n',0),(3,4,1,'/schwerpunkte/schulentwicklung/',0,2000,'Schulentwicklung',1,1,'|','dms|schulentwicklung','Aktuell\r\nUnterportale\r\n',0),(4,5,1,'/schwerpunkte/aufgabenfelder/',0,2000,'Aufgabenfelder',1,1,'|','dms|aufgabengelder','Aktuell\r\nUnterportale\r\n',0),(5,6,1,'/schwerpunkte/lernformen/',0,2000,'Lernformen',1,1,'|','dms|lernformen','Aktuell\r\nUnterportale\r\n',0),(6,7,1,'/schwerpunkte/schulformen/',0,2000,'Schulformen',1,1,'|','dms|schulformen','Aktuell\r\nUnterportale\r\n',0),(7,8,1,'/schwerpunkte/erziehung/',0,2000,'Erziehung',1,1,'|','dms|erziehung','Aktuell\r\nUnterportale\r\n',0),(8,9,1,'/einrichtungen/',0,2000,'Einrichtungen',1,1,'|','einrichtungen|','Staatliche Einrichtungen\nPartner\n',0),(9,10,1,'/zielgruppen/',0,2000,'Zielgruppen',1,1,'|','zielgruppen|','Besucher\nMitglieder von Schulgemeinden\nPartner\n',0),(10,11,1,'/zielgruppen/besucher/',0,2000,'Besucher',1,1,'|','zielgruppen|besucher','Aktuell\r\nUnterportale\r\n',0),(11,12,1,'/zielgruppen/lehrer/',0,2000,'Lehrerinnen und Lehrer',1,1,'|','zielgruppen|lehrer','Aktuell\r\nUnterportale\r\n',0),(12,13,1,'/zielgruppen/liv/',0,2000,'Lehrer im Vorbereitungsdienst (LIV)',1,1,'|','zielgruppen|liv','Aktuell\r\nUnterportale\r\n',0),(13,14,1,'/zielgruppen/schueler/',0,2000,'Sch&uuml;lerinnen und Sch&uuml;ler',1,1,'|','zielgruppen|schueler','Aktuell\r\nUnterportale\r\n',0),(14,15,1,'/zielgruppen/eltern/',0,2000,'Eltern',1,1,'|','zielgruppen|eltern','Aktuell\r\nUnterportale\r\n',0),(15,16,1,'/zielgruppen/partner/',0,2000,'Partner',1,1,'|','zielgruppen|partner','Aktuell\r\nUnterportale\r\n',0),(16,17,1,'/einrichtungen/schulaemter/',0,2000,'Staatliche Schul&auml;mter',1,1,'|','einrichtungen|ssa','Aktuell\r\nUnterportale\r\n',0),(17,18,1,'/einrichtungen/studienseminare/',0,2000,'Studienseminare',1,1,'|','einrichtungen|stsem','Aktuell\r\nUnterportale\r\n',0),(18,19,1,'/einrichtungen/hochschulen/',0,2000,'Hochschulen',1,1,'|','einrichtungen|hochschule','Aktuell\r\nUnterportale\r\n',0),(19,20,1,'/einrichtungen/partner/',0,2000,'Partner von Schule',1,1,'|','einrichtungen|partner','Aktuell\r\nUnterportale\r\n',0),(20,21,1,'/hilfe/',0,2000,'Hilfesystem',1,1,'|','|','Allgemeine Hilfe\nDjambala-Formulare\n',0),(21,22,1,'/hilfe/dms_hilfe/',0,2000,'Djambala-Hilfesystem',1,1,'|','|','Aktuell\r\nUnterportale\r\n',0),(22,23,1,'/hilfe/formular_help/',0,2000,'Djambala-Formulare',1,1,'|','|','Aktuell\r\nUnterportale\r\n',0);
/*!40000 ALTER TABLE `dms_dmscontainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsdownloadprotected`
--

DROP TABLE IF EXISTS `dms_dmsdownloadprotected`;
CREATE TABLE `dms_dmsdownloadprotected` (
  `id` int(11) NOT NULL auto_increment,
  `file` varchar(20) NOT NULL,
  `folder` varchar(5) NOT NULL,
  `order_by` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `file` (`file`),
  UNIQUE KEY `order_by` (`order_by`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsdownloadprotected`
--

LOCK TABLES `dms_dmsdownloadprotected` WRITE;
/*!40000 ALTER TABLE `dms_dmsdownloadprotected` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmsdownloadprotected` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsextitem`
--

DROP TABLE IF EXISTS `dms_dmsextitem`;
CREATE TABLE `dms_dmsextitem` (
  `id` int(11) NOT NULL auto_increment,
  `item_id` int(11) NOT NULL,
  `owner` varchar(60) default NULL,
  `owner_email` varchar(200) default NULL,
  `valid_days` int(11) NOT NULL,
  `has_timetable` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsextitem_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsextitem`
--

LOCK TABLES `dms_dmsextitem` WRITE;
/*!40000 ALTER TABLE `dms_dmsextitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmsextitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsfeed`
--

DROP TABLE IF EXISTS `dms_dmsfeed`;
CREATE TABLE `dms_dmsfeed` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `title` varchar(120) NOT NULL,
  `description` varchar(180) NOT NULL,
  `link` varchar(200) NOT NULL,
  `general_mode` int(11) NOT NULL default '0',
  `owner_id` int(11) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL default '0',
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `owner_id` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsfeed`
--

LOCK TABLES `dms_dmsfeed` WRITE;
/*!40000 ALTER TABLE `dms_dmsfeed` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmsfeed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsfeeditem`
--

DROP TABLE IF EXISTS `dms_dmsfeeditem`;
CREATE TABLE `dms_dmsfeeditem` (
  `id` int(11) NOT NULL auto_increment,
  `feed_id` int(11) NOT NULL,
  `item_container_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `is_browseable` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsfeeditem_feed_id` (`feed_id`),
  KEY `dms_dmsfeeditem_item_container_id` (`item_container_id`),
  KEY `dms_dmsfeeditem_owner_id` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsfeeditem`
--

LOCK TABLES `dms_dmsfeeditem` WRITE;
/*!40000 ALTER TABLE `dms_dmsfeeditem` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmsfeeditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsitem`
--

DROP TABLE IF EXISTS `dms_dmsitem`;
CREATE TABLE `dms_dmsitem` (
  `id` int(11) NOT NULL auto_increment,
  `app_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `license_id` int(11) NOT NULL default '1',
  `name` varchar(200) collate utf8_unicode_ci NOT NULL,
  `title` varchar(240) collate utf8_unicode_ci NOT NULL,
  `sub_title` varchar(240) collate utf8_unicode_ci NOT NULL,
  `text` longtext collate utf8_unicode_ci,
  `text_more` longtext collate utf8_unicode_ci,
  `url_more` varchar(200) collate utf8_unicode_ci NOT NULL,
  `url_more_extern` tinyint(1) NOT NULL default '0',
  `image_url` varchar(200) collate utf8_unicode_ci default NULL,
  `image_url_url` varchar(200) collate utf8_unicode_ci default NULL,
  `image_extern` tinyint(1) NOT NULL,
  `is_wide` tinyint(1) NOT NULL,
  `is_important` tinyint(1) NOT NULL,
  `info_slot_right` longtext collate utf8_unicode_ci,
  `has_user_support` tinyint(1) NOT NULL default '1',
  `has_comments` tinyint(1) NOT NULL default '0',
  `is_moderated` tinyint(1) NOT NULL default '1',
  `is_exchangeable` tinyint(1) NOT NULL default '1',
  `string_1` varchar(200) collate utf8_unicode_ci default NULL,
  `string_2` varchar(200) collate utf8_unicode_ci default NULL,
  `integer_1` int(11) NOT NULL,
  `integer_2` int(11) NOT NULL,
  `integer_3` int(11) NOT NULL,
  `integer_4` int(11) NOT NULL,
  `integer_5` int(11) NOT NULL,
  `extra` text collate utf8_unicode_ci,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsitem_app_id` (`app_id`),
  KEY `dms_dmsitem_owner_id` (`owner_id`),
  KEY `dms_dmsitem_name` (`name`),
  KEY `dms_dmsitem_string_1` (`string_1`),
  KEY `dms_dmsitem_string_2` (`string_2`),
  KEY `dms_dmsitem_integer_1` (`integer_1`),
  KEY `dms_dmsitem_integer_2` (`integer_2`),
  KEY `dms_dmsitem_integer_4` (`integer_4`),
  KEY `dms_dmsitem_integer_5` (`integer_5`),
  KEY `dms_dmsitem_integer_3` (`integer_3`),
  KEY `url_more` (`url_more`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmsitem`
--

LOCK TABLES `dms_dmsitem` WRITE;
/*!40000 ALTER TABLE `dms_dmsitem` DISABLE KEYS */;
INSERT INTO `dms_dmsitem` VALUES (1,1,1,1,'','Startseite','','<p>Herzlich willkommen auf dem Bildungsserver XYZ!</p>','','',0,'','',0,1,0,'',1,0,1,1,'','',0,0,0,0,0,''),(2,2,1,1,'impress.html','Impressum','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(3,1,1,1,'schwerpunkte','Aktuelle Schwerpunkte','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(4,1,1,1,'schulentwicklung','Schulentwicklung','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(5,1,1,1,'aufgabenfelder','Aufgabenfelder','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(6,1,1,1,'lernformen','Neue Lernformen','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(7,1,1,1,'schulformen','Schulformen','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(8,1,1,1,'erziehung','Erziehung','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(9,1,1,1,'einrichtungen','Einrichtungen','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(10,1,1,1,'zielgruppen','Zielgruppen','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(11,1,1,1,'besucher','Besucher','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(12,1,1,1,'lehrer','Lehrerinnen und Lehrer','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(13,1,1,1,'liv','Lehrer im Vorbereitungsdienst (LIV)','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(14,1,1,1,'schueler','Sch&uuml;lerinnen und Sch&uuml;ler','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(15,1,1,1,'eltern','Eltern','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(16,1,1,1,'partner','Partner','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(17,1,1,1,'schulaemter','Staatliche Schul&auml;mter','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(18,1,1,1,'studienseminare','Studienseminare','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(19,1,1,1,'hochschulen','Hochschulen','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(20,1,1,1,'partner','Partner von Schule','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(21,1,1,1,'hilfe','Hilfesystem','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(22,1,1,1,'dms_hilfe','Djambala-Hilfesystem','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(23,1,1,1,'formular_help','Djambala-Formulare','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,''),(24,2,1,1,'symbole.html','Symbole der Benutzungsoberfl&auml;che','','','','',0,'','',0,1,0,'',0,0,1,1,'','',-1,-1,-1,-1,-1,'');
/*!40000 ALTER TABLE `dms_dmsitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsitemcontainer`
--

DROP TABLE IF EXISTS `dms_dmsitemcontainer`;
CREATE TABLE `dms_dmsitemcontainer` (
  `id` int(11) NOT NULL auto_increment,
  `container_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL default '0',
  `parent_item_id` int(11) NOT NULL,
  `section` varchar(60) NOT NULL,
  `order_by` int(11) NOT NULL default '100',
  `part_of_id` int(11) NOT NULL default '-1',
  `is_browseable` tinyint(1) NOT NULL,
  `is_data_object` tinyint(1) NOT NULL default '1',
  `is_changeable` tinyint(4) NOT NULL default '1',
  `visible_start` datetime NOT NULL,
  `visible_end` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsitemcontainer_container_id` (`container_id`),
  KEY `dms_dmsitemcontainer_item_id` (`item_id`),
  KEY `dms_dmsitemcontainer_owner_id` (`owner_id`),
  KEY `parent_id` (`parent_item_id`),
  KEY `last_modified` (`last_modified`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsitemcontainer`
--

LOCK TABLES `dms_dmsitemcontainer` WRITE;
/*!40000 ALTER TABLE `dms_dmsitemcontainer` DISABLE KEYS */;
INSERT INTO `dms_dmsitemcontainer` VALUES (1,1,1,1,0,-1,'',100,0,0,1,1,'2007-11-27 00:00:00','2020-12-31 00:00:00','2007-11-28 16:14:00'),(2,1,2,1,0,1,'',100,1,0,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 12:59:06'),(3,2,3,1,0,1,'',100,1,0,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:00:45'),(4,3,4,1,0,3,'Bereiche',100,3,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:01:30'),(5,4,5,1,0,3,'Bereiche',110,3,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:02:16'),(6,5,6,1,0,3,'Bereiche',120,3,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:16:46'),(7,6,7,1,0,3,'Bereiche',130,3,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:17:20'),(8,7,8,1,0,3,'Bereiche',140,3,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:17:38'),(9,8,9,1,0,1,'',100,1,0,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:20:04'),(10,9,10,1,0,1,'',100,1,0,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:20:23'),(11,10,11,1,0,10,'Besucher',100,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:22:46'),(12,11,12,1,0,10,'Mitglieder von Schulgemeinden',110,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:23:05'),(13,12,13,1,0,10,'Mitglieder von Schulgemeinden',120,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:23:31'),(14,13,14,1,0,10,'Mitglieder von Schulgemeinden',130,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:23:51'),(15,14,15,1,0,10,'Mitglieder von Schulgemeinden',140,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:24:13'),(16,15,16,1,0,10,'Partner',150,10,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:24:33'),(17,16,17,1,0,9,'Staatliche Einrichtungen',100,9,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:27:24'),(18,17,18,1,0,9,'Staatliche Einrichtungen',110,9,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:27:47'),(19,18,19,1,0,9,'Staatliche Einrichtungen',120,9,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:28:08'),(20,19,20,1,0,9,'Partner',130,9,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:28:27'),(21,20,21,1,0,1,'',100,1,0,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:44:12'),(22,21,22,1,0,21,'Allgemeine Hilfe',100,21,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:44:46'),(23,22,23,1,0,21,'Djambala-Formulare',120,21,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:45:21'),(24,20,24,1,0,21,'Allgemeine Hilfe',110,21,1,1,1,'2007-11-28 00:00:00','2017-12-31 00:00:00','2007-11-28 13:46:01');
/*!40000 ALTER TABLE `dms_dmsitemcontainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmslicense`
--

DROP TABLE IF EXISTS `dms_dmslicense`;
CREATE TABLE `dms_dmslicense` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  `url` varchar(200) NOT NULL,
  `image_url` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmslicense`
--

LOCK TABLES `dms_dmslicense` WRITE;
/*!40000 ALTER TABLE `dms_dmslicense` DISABLE KEYS */;
INSERT INTO `dms_dmslicense` VALUES (1,'Ohne Lizenzangaben','',''),(2,'cc: Namensnennung','http://creativecommons.org/licenses/by/2.0/de/','http://i.creativecommons.org/l/by/2.0/de/88x31.png'),(3,'cc: Namensnennung-Nicht kommerziell','http://creativecommons.org/licenses/by-nc/2.0/de/','http://i.creativecommons.org/l/by-nc/2.0/de/88x31.png'),(4,'cc: Namensnennung-Nicht kommerziell-Keine Bearbeitung','http://creativecommons.org/licenses/by-nc-nd/2.0/de/','http://i.creativecommons.org/l/by-nc-nd/2.0/de/88x31.png'),(5,'cc: Namensnennung-Nicht kommerziell-Weitergabe unter gleichen Bedingungen','http://creativecommons.org/licenses/by-nc-sa/2.0/de/','http://i.creativecommons.org/l/by-nc-sa/2.0/de/88x31.png'),(6,'cc: Namensnennung-Keine Bearbeitung','http://creativecommons.org/licenses/by-nd/2.0/de/','http://i.creativecommons.org/l/by-nd/2.0/de/88x31.png'),(7,'cc: Namensnennung-Weitergabe unter gleichen Bedingungen','http://creativecommons.org/licenses/by-sa/2.0/de/','http://i.creativecommons.org/l/by-sa/2.0/de/88x31.png');
/*!40000 ALTER TABLE `dms_dmslicense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsnavmenu`
--

DROP TABLE IF EXISTS `dms_dmsnavmenu`;
CREATE TABLE `dms_dmsnavmenu` (
  `id` int(11) NOT NULL auto_increment,
  `menu_id` int(11) NOT NULL default '-1',
  `name` varchar(60) NOT NULL,
  `navigation` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `menu_id` (`menu_id`),
  KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsnavmenu`
--

LOCK TABLES `dms_dmsnavmenu` WRITE;
/*!40000 ALTER TABLE `dms_dmsnavmenu` DISABLE KEYS */;
INSERT INTO `dms_dmsnavmenu` VALUES (1,-1,'start_menu','0 | startseite | http://dms.bildung.de/ | Startseite | Startseite des Bildungsservers | <b><i><span class=\"red\">::</span></i></b>\r\n\r\n999\r\n999\r\n\r\n0 | netzwerk | http://dms.bildung.de/ | Aktuelle Schwerpunkte | Aktuelle Ma&szlig;nahmen zu Bildungspolitik und Schulentwicklung ...\r\n\r\n999\r\n\r\n1 | schulentwicklung | http://dms.bildung.de/schulentwicklung/ | Schulentwicklung\r\n1 | aufgabengelder | http://dms.bildung.de/aufgabenfelder/ | Aufgabenfelder\r\n1 | lernformen | http://dms.bildung.de/lernformen/ | Neue Lernformen\r\n1 | schulformen | http://dms.bildung.de/schulformen/ | Schulformen\r\n1 | erziehung | http://dms.bildung.de/erziehung/ | Erziehung\r\n1 | unterstuetzungssysteme | http://dms.bildung.de/unterstuetzungssysteme/ | Unterst&uuml;tzungssysteme\r\n1 | archiv | http://dms.bildung.de/archiv/ | Archiv\r\n\r\n0 | lehrerbildung | http://dms.bildung.de/ | Lehrerbildung | Aus-, Fort- und Weiterbildungsveranstaltungen f&uuml;r Lehrerinnen und Lehrer ...\r\n\r\n1 | veranstaltungen | http://dms.bildung.de/veranstaltungen/ | Veranstaltungen\r\n1 | regional | http://dms.bildung.de/reg_fortbildung/ | regionale Fortbildung\r\n1 | kalendarium | http://dms.bildung.de/kalendarium/ | Kalendarium\r\n\r\n0 | unterricht | http://lernarchiv.bildung.de/ | Unterrichtsmaterial | Lernarchive, F&auml;cher, Projekte ...\r\n\r\n1 | lehrplaene | http://lernarchiv.bildung.de/lehrplaene/ | Lehrpl&auml;ne u. Stundentafeln\r\n1 | grundschule | http://lernarchiv.bildung.de/grundschule/ | Grund- und F&ouml;rderschule\r\n1 | sek_i | http://lernarchiv.bildung.de/sek_i/ | Sekundarstufe I\r\n1 | sek_ii | http://lernarchiv.bildung.de/sek_ii/ | Sekundarstufe II\r\n1 | beruf | http://lernarchiv.bildung.de/beruf_bildung/ | Berufliche Bildung\r\n1 | uebergreifend | http://lernarchiv.bildung.de/uebergreifend/ | &Uuml;bergreifende Angebote\r\n\r\n0 | schule | http://dms.bildung.de/ | Schule | Schulserver, Schulprogramme, Schulkultur ...\r\n\r\n1 | grundschule | http://dms.bildung.de/grundschule/ | Grundschule\r\n1 | foerderschule | http://dms.bildung.de/foerderschule/ | F&ouml;rderschule\r\n1 | hauptschule | http://dms.bildung.de/hauptschule/ | Hauptschule\r\n1 | realschule | http://dms.bildung.de/realschule/ | Realschule\r\n1 | gymnasium | http://dms.bildung.de/gymnasium/  | Gymnasium\r\n1 | igs | http://dms.bildung.de/igs/ | Integrierte Gesamtschule\r\n1 | beruf | http://dms.bildung.de/berufliche_bildung/ | Berufliche Bildung\r\n1 | oberstufe | http://dms.bildung.de/gym_sek_ii/ | Gymnasiale Oberstufe\r\n1 | sfe | http://dms.bildung.de/sfe/ | Schulen f&uuml;r Erwachsene\r\n1 | allgemein | http://dms.bildung.de/allgemeines/ | Allgemeine Aspekte\r\n\r\n0 | region | http://dms.bildung.de/ | Bildungsregionen | Bildungsregionen, Schul&auml;mter, regionale Fortbildung ...\r\n\r\n1 | bergstrasse | http://dms.bildung.de/bergstrasse/ |Bergstra&szlig;e|Bergstra&szlig;e und Odenwaldkreis\r\n1 | darmstadt | http://dms.bildung.de/darmstadt/ |Darmstadt|Darmstadt-Dieburg\r\n1 | frankfurt | http://dms.bildung.de/frankfurt/ |Frankfurt|Frankfurt\r\n1 | fulda | http://dms.bildung.de/fulda/ |Fulda|Fulda\r\n1 | giessen | http://dms.bildung.de/giessen/ |Gie&szlig;en|Gie&szlig;en und Vogelsbergkreis\r\n1 | gross_gerau | http://dms.bildung.de/gross_gerau/ |Gro&szlig;-Gerau|Groszlig;-Gerau und Main-Taunus-Kreis\r\n1 | bebra | http://dms.bildung.de/bebra/ |Hersfeld|Hersfeld-Rotenburg und Werra-Mei&szlig;ner-Kreis\r\n1 | hochtaunus | http://dms.bildung.de/hochtaunus/ |Hochtaunus|Hochtaunuskreis und Wetteraukreis\r\n1 | kassel | http://dms.bildung.de/kassel/ |Kassel|Kassel\r\n1 | lahn_dill | http://dms.bildung.de/lahn_dill/|Lahn-Dill|Lahn-Dill und Limburg-Weilburg\r\n1 | main_kinzig | http://dms.bildung.de/main_kinzig/|Main-Kinzig|Main-Kinzig-Kreis\r\n1 | marburg | http://dms.bildung.de/marburg/|Marburg|Marburg/Biedenkopf\r\n1 | offenbach | http://dms.bildung.de/offenbach/ |Offenbach|Offenbach\r\n1 | wiesbaden | http://dms.bildung.de/wiesbaden/ |Wiesbaden|Rheingau-Taunus-Kreis und Wiesbaden\r\n1 | schwalm | http://dms.bildung.de/schwalm/|Schwalm-Eder|Schwalm-Eder-Kreis und Landkreis Waldeck-Frankenberg\r\n\r\n999\r\n\r\n0 | einrichtungen | http://dms.bildung.de/einrichtung/ | Einrichtungen | Einrichtungen und Institutionen im p&auml;dagogischen Bereich\r\n\r\n1 | staatlich | http://dms.bildung.de/einrichtung/staatlich/ | staatliche Organisationen\r\n1 | hochschule | http://dms.bildung.de/einrichtung/hochschule/ | Hochschulen\r\n1 | partner | http://dms.bildung.de/einrichtung/partner/ | Partner von Schule\r\n1 | besonderes | http://dms.bildung.de/einrichtung/besonderes/ | besondere Anliegen\r\n\r\n0 | zielgruppen | http://dms.bildung.de/zielgruppe/ | Zielgruppen | Angebote f&uuml;r Eltern, Lehrer/innen, Partner von Schule\r\n\r\n1 | adressaten | http://dms.bildung.de/zielgruppe/adressaten/ |  Adressaten\r\n1 | ags | http://dms.bildung.de/zielgruppe/ags/ | Arbeitsgemeinschaften\r\n\r\n0 | service | http://dms.bildung.de/ | Service | Service-Angebote, Kommunikation, Sonstiges ...\r\n\r\n1 | publikationen | http://dms.bildung.de/publikationen/ | Publikationen\r\n1 | hilfen | http://dms.bildung.de/hilfen/ | Hilfen\r\n1 | recht | http://dms.bildung.de/recht/ | Recht\r\n1 | software | http://dms.bildung.de/software/ | Software\r\n\r\n0 | medien | http://dms.bildung.de/ | Medienbildung | Medienbildung, Computer, Netze ...\r\n\r\n1 | einrichtungen | http://dms.bildung.de/einrichtungen/ | Einrichtungen\r\n1 | projekte | http://dms.bildung.de/projekte/ | Projekte\r\n1 | service | http://dms.bildung.de/service/ | Service\r\n1 | internes | http://dms.bildung.de/internes/ | Arbeitsgruppen / Internes\r\n\r\n999\r\n\r\n0 | community | http://dms.bildung.de/ | Community | Mitarbeit, Zugang zu geschlossenen Bereichen ...\r\n\r\n1 | registrierung | http://dms.bildung.de/registrierung/ | Registrierung\r\n1 | eigenes | http://dms.bildung.de/eigenes/ | Eigene Daten\r\n1 | admin | http://dms.bildung.de/admin/ | Administration\r\n\r\n0 | wir_ueber_uns | http://dms.bildung.de/wir_ueber_uns/ | Wir &uuml;ber uns | Allgemeine Informationen zum Bildungsserver ...\r\n\r\n1 | mitarbeit | http://dms.bildung.de/wir_ueber_uns/mitarbeit/ |  Mitarbeit\r\n1 | statistik | http://dms.bildung.de/wir_ueber_uns/statistik/ | Statistik\r\n1 | vortraege | http://dms.bildung.de/wir_ueber_uns/vortraege/ | Vortr&auml;ge\r\n');
/*!40000 ALTER TABLE `dms_dmsnavmenu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsnavmenuleft`
--

DROP TABLE IF EXISTS `dms_dmsnavmenuleft`;
CREATE TABLE `dms_dmsnavmenuleft` (
  `id` int(11) NOT NULL auto_increment,
  `menu_id` int(11) NOT NULL default '-1',
  `is_main_menu` tinyint(1) NOT NULL default '0',
  `name` varchar(60) NOT NULL,
  `description` varchar(80) NOT NULL,
  `navigation` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `menu_id` (`menu_id`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=232 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsnavmenuleft`
--

LOCK TABLES `dms_dmsnavmenuleft` WRITE;
/*!40000 ALTER TABLE `dms_dmsnavmenuleft` DISABLE KEYS */;
INSERT INTO `dms_dmsnavmenuleft` VALUES (1,-1,1,'start_menu','Start','0 | startseite | http://dms.bildung.de/ | Startseite | Startseite des Bildungsservers | <b><i><span class=\"red\">::</span></i></b>\r\n\r\n999\r\n\r\n0 | dms | http://dms.bildung.de/schwerpunkte/ | Aktuelle Schwerpunkte | Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\r\n\r\n1 | schulentwicklung | http://dms.bildung.de/schwerpunkte/schulentwicklung/ | Schulentwicklung\r\n1 | aufgabengelder | http://dms.bildung.de/schwerpunkte/aufgabenfelder/ | Aufgabenfelder\r\n1 | lernformen | http://dms.bildung.de/schwerpunkte/lernformen/ | Neue Lernformen\r\n1 | schulformen | http://dms.bildung.de/schwerpunkte/schulformen/ | Schulformen\r\n1 | erziehung | http://dms.bildung.de/schwerpunkte/erziehung/ | Erziehung\r\n\r\n0 | einrichtungen | http://dms.bildung.de/einrichtungen/ | Einrichtungen | Einrichtungen und Institutionen im pädagogischen Bereich\r\n\r\n1 | hkm | http://www.kultusministerium.hessen.de/ | HKM | Hessisches Kultusministerium\r\n1 | afl | http://www.afl.hessen.de/ | AfL | Amt für Lehrerbildung\r\n1 | iq | http://www.iq.hessen.de/ | IQ | Institut für Qualitätsentwicklung\r\n1 | ssa | http://dms.bildung.de/einrichtungen/schulaemter/ | Schulämter\r\n1 | stsem | http://dms.bildung.de/einrichtungen/studienseminare/ | Studienseminare\r\n1 | hochschule | http://dms.bildung.de/einrichtungen/hochschulen/ | Hochschulen\r\n1 | partner | http://dms.bildung.de/einrichtungen/partner/ | Partner von Schule\r\n\r\n0 | zielgruppen | http://dms.bildung.de/zielgruppen/ | Zielgruppen | Angebote für Eltern, Lehrer/innen, Partner von Schule\r\n\r\n1 | besucher | http://dms.bildung.de/zielgruppen/besucher/ |  Besucher\r\n1 | lehrer | http://dms.bildung.de/zielgruppen/lehrer/ |  Lehrer/innen\r\n1 | liv | http://dms.bildung.de/zielgruppen/liv/ |  LiV\r\n1 | schueler | http://dms.bildung.de/zielgruppen/schueler |  Schüler/innen\r\n1 | eltern | http://dms.bildung.de/zielgruppen/eltern/ |  Eltern\r\n1 | partner | http://dms.bildung.de/zielgruppen/partner/ |  Partner\r\n'),(209,1,1,'|','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(210,1,1,'startseite|','','<div class=\"menu_area\">\n<div style=\"padding-left:2px;\">\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div style=\"margin-left:15px;\">\n<div style=\"padding:0.3em;\"></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(211,1,1,'dms|','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\">\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(212,1,1,'dms|schulentwicklung','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(213,1,1,'dms|aufgabengelder','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(214,1,1,'dms|lernformen','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(215,1,1,'dms|schulformen','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(216,1,1,'dms|erziehung','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulentwicklung/\" title=\"\">Schulentwicklung</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/aufgabenfelder/\" title=\"\">Aufgabenfelder</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/lernformen/\" title=\"\">Neue Lernformen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/schulformen/\" title=\"\">Schulformen</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/erziehung/\" title=\"\">Erziehung</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(217,1,1,'einrichtungen|','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\">\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(218,1,1,'einrichtungen|hkm','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(219,1,1,'einrichtungen|afl','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(220,1,1,'einrichtungen|iq','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(221,1,1,'einrichtungen|ssa','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(222,1,1,'einrichtungen|stsem','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(223,1,1,'einrichtungen|hochschule','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(224,1,1,'einrichtungen|partner','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.kultusministerium.hessen.de/\" title=\"Hessisches Kultusministerium\">HKM</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.afl.hessen.de/\" title=\"Amt für Lehrerbildung\">AfL</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://www.iq.hessen.de/\" title=\"Institut für Qualitätsentwicklung\">IQ</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/schulaemter/\" title=\"\">Schulämter</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/studienseminare/\" title=\"\">Studienseminare</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/hochschulen/\" title=\"\">Hochschulen</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/partner/\" title=\"\">Partner von Schule</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n</div>\n</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n'),(225,1,1,'zielgruppen|','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\">\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(226,1,1,'zielgruppen|besucher','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(227,1,1,'zielgruppen|lehrer','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(228,1,1,'zielgruppen|liv','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(229,1,1,'zielgruppen|schueler','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(230,1,1,'zielgruppen|eltern','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span></div>\n</div>\n</div>\n</div>\n'),(231,1,1,'zielgruppen|partner','','<div class=\"menu_border_bottom\"> <b><i><span class=\"red\">::</span></i></b>&nbsp;<a class=\"navLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\"><b>Startseite</b></a><span class=\"invisible\">|</span></div>\n<div style=\"padding:0.3em;\"></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/schwerpunkte/\" title=\"Aktuelle Maßnahmen zu Bildungspolitik und Schulentwicklung ...\">Aktuelle Schwerpunkte</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/einrichtungen/\" title=\"Einrichtungen und Institutionen im pädagogischen Bereich\">Einrichtungen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_area\">\n<div style=\"padding-left:2px;\"><div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/\" title=\"Angebote für Eltern, Lehrer/innen, Partner von Schule\">Zielgruppen</a><span class=\"invisible\">|</span></div>\n<div style=\"margin-left:15px;\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/besucher/\" title=\"\">Besucher</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/lehrer/\" title=\"\">Lehrer/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/liv/\" title=\"\">LiV</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/schueler\" title=\"\">Schüler/innen</a><span class=\"invisible\">|</span></div>\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/eltern/\" title=\"\">Eltern</a><span class=\"invisible\">|</span></div>\n\n<div class=\"tabHeaderBg\">\n<div class=\"menu_border_bottom\"><a class=\"navLink\" href=\"http://dms.bildung.de/zielgruppen/partner/\" title=\"\">Partner</a><span class=\"invisible\">|</span>&raquo;</div>\n</div>\n</div>\n</div>\n</div>\n');
/*!40000 ALTER TABLE `dms_dmsnavmenuleft` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsnavmenutop`
--

DROP TABLE IF EXISTS `dms_dmsnavmenutop`;
CREATE TABLE `dms_dmsnavmenutop` (
  `id` int(11) NOT NULL auto_increment,
  `menu_id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `navigation` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_dmsnavmenutop_menu_id` (`menu_id`),
  KEY `dms_dmsnavmenutop_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmsnavmenutop`
--

LOCK TABLES `dms_dmsnavmenutop` WRITE;
/*!40000 ALTER TABLE `dms_dmsnavmenutop` DISABLE KEYS */;
INSERT INTO `dms_dmsnavmenutop` VALUES (1,-1,'start_menu','start | http://dms.bildung.de/ | Start | Startseite des Bildungsservers\r\n\r\nwir-ueber-uns | http://dms.bildung.de/index.html | Über uns | Allgemeine Informationen zum Bildungsserver\r\n\r\nunterricht | http://dms.bildung.de/index.html | Unterrichtsmaterial | Unterrichtsmaterial für Fächer, Schulstufen- und -formen\r\n\r\nlehrerbildung | http://dms.bildung.de/index.html | Lehrerbildung | Lehrerfort- und -weiterbildung\r\n\r\nschule | http://dms.bildung.de/index.html | Schule | Informationen zu den Schulen\r\n\r\nregion | http://dms.bildung.de/index.html | Region | 99 Bildungsregionen\r\n\r\nlakk | http://dms.bildung.de/index.html | lakk <i>online</i> | Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\r\n\r\nservice | http://dms.bildung.de/index.html | Service | Allgemeine Serviceangebote\r\n\r\ncommunity | http://dms.bildung.de/index.html | Community| Community des Bildungsservers\r\n\r\n'),(85,1,'|','<span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Start&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(86,1,'start','<span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Start&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(87,1,'wir-ueber-uns','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Über uns&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(88,1,'unterricht','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Unterrichtsmaterial&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(89,1,'lehrerbildung','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Lehrerbildung&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(90,1,'schule','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Schule&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(91,1,'region','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Region&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(92,1,'lakk','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;lakk <i>online</i>&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(93,1,'service','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Service&nbsp;&nbsp;</span></span> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Community des Bildungsservers\">Community</a>'),(94,1,'community','<a class=\"navTopLink\" href=\"http://dms.bildung.de/\" title=\"Startseite des Bildungsservers\">Start</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Informationen zum Bildungsserver\">Über uns</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Unterrichtsmaterial für Fächer, Schulstufen- und -formen\">Unterrichtsmaterial</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Lehrerfort- und -weiterbildung\">Lehrerbildung</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Informationen zu den Schulen\">Schule</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"99 Bildungsregionen\">Region</a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Übergreifende Lern-, Arbeits-, Kommunikations-  und Kooperationsplattformen\">lakk <i>online</i></a> <span class=\"navTop\">|</span> <a class=\"navTopLink\" href=\"http://dms.bildung.de/index.html\" title=\"Allgemeine Serviceangebote\">Service</a> <span class=\"navTop\">|</span> <span class=\"navTopBoxSelected\"><span class=\"navTopLinkSelected\">&nbsp;&nbsp;Community&nbsp;&nbsp;</span></span>');
/*!40000 ALTER TABLE `dms_dmsnavmenutop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmsowner`
--

DROP TABLE IF EXISTS `dms_dmsowner`;
CREATE TABLE `dms_dmsowner` (
  `id` int(11) NOT NULL auto_increment,
  `user` varchar(60) collate utf8_unicode_ci NOT NULL,
  `name` varchar(80) collate utf8_unicode_ci NOT NULL,
  `email` varchar(75) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmsowner`
--

LOCK TABLES `dms_dmsowner` WRITE;
/*!40000 ALTER TABLE `dms_dmsowner` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_dmsowner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmssearchengine`
--

DROP TABLE IF EXISTS `dms_dmssearchengine`;
CREATE TABLE `dms_dmssearchengine` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(40) NOT NULL,
  `url_query` varchar(240) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_dmssearchengine`
--

LOCK TABLES `dms_dmssearchengine` WRITE;
/*!40000 ALTER TABLE `dms_dmssearchengine` DISABLE KEYS */;
INSERT INTO `dms_dmssearchengine` VALUES (1,'Google','http://www.google.de/search?q=%s&hl=de&as_dt=i&as_sitesearch=%s'),(2,'Yahoo','http://search.yahoo.com/search?p=%s+site:%s');
/*!40000 ALTER TABLE `dms_dmssearchengine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_dmssite`
--

DROP TABLE IF EXISTS `dms_dmssite`;
CREATE TABLE `dms_dmssite` (
  `id` int(11) NOT NULL auto_increment,
  `url` varchar(200) collate utf8_unicode_ci NOT NULL,
  `base_folder` varchar(200) collate utf8_unicode_ci NOT NULL,
  `name` varchar(60) collate utf8_unicode_ci NOT NULL,
  `title` varchar(200) collate utf8_unicode_ci NOT NULL,
  `sub_title` varchar(200) collate utf8_unicode_ci NOT NULL,
  `title_class` varchar(40) collate utf8_unicode_ci NOT NULL,
  `logo` varchar(120) collate utf8_unicode_ci NOT NULL,
  `logo_url` varchar(200) collate utf8_unicode_ci NOT NULL,
  `logo_width` int(11) NOT NULL,
  `logo_height` int(11) NOT NULL,
  `skin_style` varchar(30) collate utf8_unicode_ci NOT NULL,
  `left_image_url` varchar(200) collate utf8_unicode_ci NOT NULL,
  `left_image_width` int(11) NOT NULL,
  `left_image_height` int(11) NOT NULL,
  `navigation_bottom_image` varchar(240) collate utf8_unicode_ci NOT NULL,
  `impress_url` varchar(200) collate utf8_unicode_ci NOT NULL,
  `master_links` text collate utf8_unicode_ci NOT NULL,
  `help_url` varchar(200) collate utf8_unicode_ci NOT NULL,
  `search_form` text collate utf8_unicode_ci NOT NULL,
  `org_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dms_dmssite`
--

LOCK TABLES `dms_dmssite` WRITE;
/*!40000 ALTER TABLE `dms_dmssite` DISABLE KEYS */;
INSERT INTO `dms_dmssite` VALUES (1,'http://dms.bildung.de','','Bildungsserver','Bildungsserver XYZ','','head1','/dms_media/skin_style/logo/logo_bs.gif','http://dms.bildung.de/index.html',98,104,'bs','/dms_media/skin_style/base/left_image_bs.gif',31,212,'<br />','http://dms.bildung.de/impress.html','','http://dms-hilfe.bildung.de/','<div id=\"layer_top_search\"><div><form name=\"g_input\" method=\"get\" action=\"./searchxapian/\" class=\"form-no-margin\"><label for=\"q1\"></label><input class=\"select\" type=\"text\" id=\"q1\" name=\"query\" size=\"20\" maxlength=\"255\" value=\"Suche\" onfocus=\"if (document.g_input.q1.value==\"Suche\"){document.g_input.q1.value=\"\";}\" onblur=\"if (document.g_input.q1.value!=\"Suche\"){document.g_input.q1.value=\"Suche\";}\"></form></div></div><br clear=\"all\" />',0),(2,'http://dms-hilfe.bildung.de','/hilfe','Hilfesystem','Bildungsserver XYZ','Hilfesystem','head1','/dms_media/skin_style/logo/logo_bs.gif','http://dms.bildung.de/index.html',98,104,'bs','/dms_media/skin_style/base/left_image_bs.gif',31,212,'','http://dms.bildung.de/impress.html','','http://dms-hilfe.bildung.de/','<div id=\"layer_top_search\"><div><form name=\"g_input\" method=\"get\" action=\"./searchxapian/\" class=\"form-no-margin\"><label for=\"q1\"></label><input class=\"select\" type=\"text\" id=\"q1\" name=\"query\" size=\"20\" maxlength=\"255\" value=\"Suche\" onfocus=\"if (document.g_input.q1.value==\"Suche\"){document.g_input.q1.value=\"\";}\" onblur=\"if (document.g_input.q1.value!=\"Suche\"){document.g_input.q1.value=\"Suche\";}\"></form></div></div><br clear=\"all\" />',0);
/*!40000 ALTER TABLE `dms_dmssite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_fach_sachgebiet`
--

DROP TABLE IF EXISTS `dms_edu_fach_sachgebiet`;
CREATE TABLE `dms_edu_fach_sachgebiet` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `order_by` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `order_by` (`order_by`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_fach_sachgebiet`
--

LOCK TABLES `dms_edu_fach_sachgebiet` WRITE;
/*!40000 ALTER TABLE `dms_edu_fach_sachgebiet` DISABLE KEYS */;
INSERT INTO `dms_edu_fach_sachgebiet` VALUES (1,'Deutsch',10),(2,'Englisch',10),(3,'Franz&ouml;sisch',10),(4,'Griechisch',10),(5,'Italienisch',10),(6,'Latein',10),(7,'Russisch',10),(9,'Spanisch',10),(10,'Kunst',10),(11,'Musik',10),(12,'Sport',10),(13,'Darstellendes Spiel',10),(14,'Geographie',10),(15,'Geschichte',10),(16,'Politik und Wirtschaft',10),(17,'Arbeitslehre',10),(18,'Mathematik',10),(19,'Biologie',10),(20,'Chemie',10),(21,'Physik',10),(22,'Naturwissenschaft (NaWi)',10),(23,'Informatik',10),(24,'Ethik',10),(25,'Religion ev.',10),(26,'Religion kath.',10),(27,'Sachunterricht',10),(28,'F&auml;cher&uuml;bergreifend',2),(29,'Ohne Fachbezug',1),(30,'Hebr&auml;isch',10),(31,'Herkunftssprachlicher Unterricht',10),(32,'Portugiesisch',10),(33,'Deutsch als Fremd- u. Zweitsprache',10),(34,'T&uuml;rkisch',10),(35,'Werken/Textiles Gestalten',10),(36,'BF Bautechnik',21),(37,'BF Chemie-, Biologie- und Physiktechnik',21),(38,'BF Druck- und Medientechnik',21),(39,'BF Elektrotechnik',21),(40,'BF Ern&auml;hrung und Hauswirtschaft',21),(41,'BF Fahrzeugtechnik',21),(42,'BF Farbtechnik und Raumgestaltung',21),(43,'BF Gartenbau und Floristik',21),(44,'BF Holztechnik',21),(45,'BF K&ouml;rperpflege',21),(46,'BF Metalltechnik',21),(47,'BF Neugeordnete Berufe',21),(48,'BF Sozialp&auml;gogische Berufe',21),(49,'BF Textiltechnik und Bekleidung',21),(50,'BF Wirtschaft und Verwaltung',21),(51,'BF Medizinisch-technische und krankenpfleger. Berufe',21),(52,'BF Informatik',21),(53,'Berufliche Fachrichtungen',20),(54,'BF Sozialp&auml;dagogik/Sozialwesen',21),(55,'BF Gesundheit',21),(56,'BF Drucktechnik',21),(57,'BF Agrarwirtschaft',21),(58,'BF Sonstige',21),(59,'Allgemeine Kompetenzen',2),(60,'Erziehungsaufgaben',2),(61,'Kindergarten',5),(62,'Anfangsunterricht (Grundschule)',7),(63,'Themen der Grundschule',8),(64,'Bilingualer Unterricht',10);
/*!40000 ALTER TABLE `dms_edu_fach_sachgebiet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_lernrestyp`
--

DROP TABLE IF EXISTS `dms_edu_lernrestyp`;
CREATE TABLE `dms_edu_lernrestyp` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_lernrestyp`
--

LOCK TABLES `dms_edu_lernrestyp` WRITE;
/*!40000 ALTER TABLE `dms_edu_lernrestyp` DISABLE KEYS */;
INSERT INTO `dms_edu_lernrestyp` VALUES (1,'Arbeitsblatt',5),(2,'Online-Kurs',114),(3,'Folie',112),(4,'Arbeitsmaterial',6),(5,'Zusatzmaterial',123),(6,'Arbeit/Lernkontrolle',108),(7,'Anderer Lernort',100),(8,'Pr&auml;sentation',116),(9,'Software',120),(10,'CD/DVD/Film ...',109),(11,'Radio/TV ...',118),(12,'Portal',115),(13,'Institution',112),(14,'Lehrplan',7),(15,'Unterrichtsentwurf',2),(16,'Examensarbeit',111),(17,'Thematischer Hintergrund',121),(18,'Didaktik/Methodik',110),(19,'Unterrichtseinheit',1),(20,'Projekt',4),(21,'Lern/Planspiel',113),(22,'Recht',119),(23,'Webquest',3),(24,'Hauptdokument',0),(25,'Prim&auml;rmaterial',117);
/*!40000 ALTER TABLE `dms_edu_lernrestyp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_medienformat`
--

DROP TABLE IF EXISTS `dms_edu_medienformat`;
CREATE TABLE `dms_edu_medienformat` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_medienformat`
--

LOCK TABLES `dms_edu_medienformat` WRITE;
/*!40000 ALTER TABLE `dms_edu_medienformat` DISABLE KEYS */;
INSERT INTO `dms_edu_medienformat` VALUES (1,'CD/DVD'),(2,'Video/Magnetband'),(3,'Tonkassette/Tonband'),(4,'Dia/Foto'),(5,'Printmedium'),(6,'Online-Ressource'),(8,'Medienpaket'),(9,'Audio/CD'),(10,'Video-DVD/CD'),(11,'Videokassette');
/*!40000 ALTER TABLE `dms_edu_medienformat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_objekt`
--

DROP TABLE IF EXISTS `dms_edu_objekt`;
CREATE TABLE `dms_edu_objekt` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_objekt`
--

LOCK TABLES `dms_edu_objekt` WRITE;
/*!40000 ALTER TABLE `dms_edu_objekt` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_edu_objekt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_schlagwort`
--

DROP TABLE IF EXISTS `dms_edu_schlagwort`;
CREATE TABLE `dms_edu_schlagwort` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_schlagwort`
--

LOCK TABLES `dms_edu_schlagwort` WRITE;
/*!40000 ALTER TABLE `dms_edu_schlagwort` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_edu_schlagwort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_schlagwort_stem`
--

DROP TABLE IF EXISTS `dms_edu_schlagwort_stem`;
CREATE TABLE `dms_edu_schlagwort_stem` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `stem` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `dms_edu_schlagwort_stem_stem` (`stem`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_schlagwort_stem`
--

LOCK TABLES `dms_edu_schlagwort_stem` WRITE;
/*!40000 ALTER TABLE `dms_edu_schlagwort_stem` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_edu_schlagwort_stem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_schulart`
--

DROP TABLE IF EXISTS `dms_edu_schulart`;
CREATE TABLE `dms_edu_schulart` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_schulart`
--

LOCK TABLES `dms_edu_schulart` WRITE;
/*!40000 ALTER TABLE `dms_edu_schulart` DISABLE KEYS */;
INSERT INTO `dms_edu_schulart` VALUES (1,'Hauptschule',2),(2,'Realschule',3),(3,'Gymnasium',4),(4,'F&ouml;rderschule',1),(5,'Berufsbildende Schulen',5);
/*!40000 ALTER TABLE `dms_edu_schulart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_schulstufe`
--

DROP TABLE IF EXISTS `dms_edu_schulstufe`;
CREATE TABLE `dms_edu_schulstufe` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_schulstufe`
--

LOCK TABLES `dms_edu_schulstufe` WRITE;
/*!40000 ALTER TABLE `dms_edu_schulstufe` DISABLE KEYS */;
INSERT INTO `dms_edu_schulstufe` VALUES (1,'Elementarbildung',2),(2,'Primarstufe',3),(3,'Sekundarstufe I',4),(4,'Sekundarstufe II',5),(5,'Erwachsenenbildung',6);
/*!40000 ALTER TABLE `dms_edu_schulstufe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_sprache`
--

DROP TABLE IF EXISTS `dms_edu_sprache`;
CREATE TABLE `dms_edu_sprache` (
  `id` int(11) NOT NULL auto_increment,
  `key` varchar(10) NOT NULL,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_sprache`
--

LOCK TABLES `dms_edu_sprache` WRITE;
/*!40000 ALTER TABLE `dms_edu_sprache` DISABLE KEYS */;
INSERT INTO `dms_edu_sprache` VALUES (1,'de','Deutsch'),(2,'en','Englisch'),(3,'fr','Franz&ouml;sisch'),(4,'el','Griechisch'),(5,'eo','Esperanto'),(6,'es','Spanisch'),(7,'he','Hebr&auml;isch'),(8,'it','Italienisch'),(9,'la','Lateinisch'),(10,'pl','Polnisch'),(11,'pt','Portugiesisch'),(12,'ru','Russisch'),(13,'tr','T&uuml;rkisch');
/*!40000 ALTER TABLE `dms_edu_sprache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_zertifikat`
--

DROP TABLE IF EXISTS `dms_edu_zertifikat`;
CREATE TABLE `dms_edu_zertifikat` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `policy_url` varchar(200) NOT NULL,
  `logo_url` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_zertifikat`
--

LOCK TABLES `dms_edu_zertifikat` WRITE;
/*!40000 ALTER TABLE `dms_edu_zertifikat` DISABLE KEYS */;
INSERT INTO `dms_edu_zertifikat` VALUES (1,'ohne Zertifikat','',''),(2,'empfohlen vom AfL','http://afl.bildung.hessen.de/policy/','http://afl.bildung.hessen.de/logo_thumbs/afl.gif');
/*!40000 ALTER TABLE `dms_edu_zertifikat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_edu_zielgruppe`
--

DROP TABLE IF EXISTS `dms_edu_zielgruppe`;
CREATE TABLE `dms_edu_zielgruppe` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_edu_zielgruppe`
--

LOCK TABLES `dms_edu_zielgruppe` WRITE;
/*!40000 ALTER TABLE `dms_edu_zielgruppe` DISABLE KEYS */;
INSERT INTO `dms_edu_zielgruppe` VALUES (1,'Vorschulkinder',2),(2,'Sch&uuml;ler/innen',3),(3,'Lehrer/innen',6),(4,'Referendar/innen (LIV)',5),(5,'Studierende',4),(7,'Kindergartenkinder',1);
/*!40000 ALTER TABLE `dms_edu_zielgruppe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_bildungsebene`
--

DROP TABLE IF EXISTS `dms_elixier_bildungsebene`;
CREATE TABLE `dms_elixier_bildungsebene` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `bildungsebene` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_bildungsebene`
--

LOCK TABLES `dms_elixier_bildungsebene` WRITE;
/*!40000 ALTER TABLE `dms_elixier_bildungsebene` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_bildungsebene` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_fach`
--

DROP TABLE IF EXISTS `dms_elixier_fach`;
CREATE TABLE `dms_elixier_fach` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `fach` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_fach`
--

LOCK TABLES `dms_elixier_fach` WRITE;
/*!40000 ALTER TABLE `dms_elixier_fach` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_fach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_item`
--

DROP TABLE IF EXISTS `dms_elixier_item`;
CREATE TABLE `dms_elixier_item` (
  `id` int(11) NOT NULL auto_increment,
  `id_local` varchar(64) NOT NULL,
  `status` int(11) NOT NULL,
  `fach_sachgebiet` int(11) NOT NULL default '-1',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_local` (`id_local`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_item`
--

LOCK TABLES `dms_elixier_item` WRITE;
/*!40000 ALTER TABLE `dms_elixier_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_medienformat`
--

DROP TABLE IF EXISTS `dms_elixier_medienformat`;
CREATE TABLE `dms_elixier_medienformat` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `medienformat` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_medienformat`
--

LOCK TABLES `dms_elixier_medienformat` WRITE;
/*!40000 ALTER TABLE `dms_elixier_medienformat` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_medienformat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_org`
--

DROP TABLE IF EXISTS `dms_elixier_org`;
CREATE TABLE `dms_elixier_org` (
  `id` int(11) NOT NULL auto_increment,
  `anbieter_herkunft` varchar(120) NOT NULL,
  `autor` varchar(80) NOT NULL,
  `autor_email` varchar(200) NOT NULL,
  `beschreibung` longtext NOT NULL,
  `beschreibung_lang` longtext NOT NULL,
  `bild_url` varchar(200) NOT NULL,
  `bildungsebene` longtext NOT NULL,
  `einsteller` varchar(80) NOT NULL,
  `einsteller_email` varchar(200) NOT NULL,
  `fach_sachgebiet` longtext NOT NULL,
  `herausgeber` varchar(120) NOT NULL,
  `id_local` varchar(64) NOT NULL,
  `isbn` varchar(30) NOT NULL,
  `kmk_standards` longtext NOT NULL,
  `lehrplanbezug` longtext NOT NULL,
  `lernressourcentyp` longtext NOT NULL,
  `lernzeit` varchar(60) NOT NULL,
  `lernziel` longtext NOT NULL,
  `letzte_aenderung` datetime default NULL,
  `medienformat` longtext NOT NULL,
  `methodik` longtext NOT NULL,
  `preis` varchar(60) NOT NULL,
  `publikationsdatum` date default NULL,
  `quelle_homepage_url` varchar(200) NOT NULL,
  `quelle_id` varchar(16) NOT NULL,
  `quelle_logo_url` varchar(200) NOT NULL,
  `quelle_pfad` varchar(60) NOT NULL,
  `rechte` longtext NOT NULL,
  `schlagwort` longtext NOT NULL,
  `schulform` longtext NOT NULL,
  `sprache` longtext NOT NULL,
  `systematikpfad` longtext NOT NULL,
  `techn_voraussetzungen` longtext NOT NULL,
  `titel` varchar(240) NOT NULL,
  `titel_lang` longtext NOT NULL,
  `url_datensatz` varchar(200) NOT NULL,
  `url_ressource` varchar(200) NOT NULL,
  `verfallsdatum` date default NULL,
  `weitere_kompetenzen` longtext NOT NULL,
  `zertifizierung` longtext NOT NULL,
  `zielgruppe` longtext NOT NULL,
  `zeitstempel` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_local` (`id_local`),
  KEY `dms_elixier_org_einsteller` (`einsteller`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_org`
--

LOCK TABLES `dms_elixier_org` WRITE;
/*!40000 ALTER TABLE `dms_elixier_org` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_quelle`
--

DROP TABLE IF EXISTS `dms_elixier_quelle`;
CREATE TABLE `dms_elixier_quelle` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(16) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `quelle` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_quelle`
--

LOCK TABLES `dms_elixier_quelle` WRITE;
/*!40000 ALTER TABLE `dms_elixier_quelle` DISABLE KEYS */;
INSERT INTO `dms_elixier_quelle` VALUES (4,'DBS'),(5,'LBS-BW'),(6,'NDS'),(7,'SN'),(8,'SODIS');
/*!40000 ALTER TABLE `dms_elixier_quelle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_elixier_schlagwort`
--

DROP TABLE IF EXISTS `dms_elixier_schlagwort`;
CREATE TABLE `dms_elixier_schlagwort` (
  `id` int(11) NOT NULL auto_increment,
  `schlagwort` varchar(64) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `schlagwort` (`schlagwort`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_elixier_schlagwort`
--

LOCK TABLES `dms_elixier_schlagwort` WRITE;
/*!40000 ALTER TABLE `dms_elixier_schlagwort` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_elixier_schlagwort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_fort_fach`
--

DROP TABLE IF EXISTS `dms_fort_fach`;
CREATE TABLE `dms_fort_fach` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_fort_fach`
--

LOCK TABLES `dms_fort_fach` WRITE;
/*!40000 ALTER TABLE `dms_fort_fach` DISABLE KEYS */;
INSERT INTO `dms_fort_fach` VALUES (1,'Alle'),(54,'Arbeitslehre'),(56,'Berufliche Fachrichtungen'),(60,'BF Agrarwirtschaft'),(2,'BF Bautechnik'),(3,'BF Chemie-, Biologie- und Physiktechnik'),(4,'BF Druck- und Medientechnik'),(59,'BF Drucktechnik'),(5,'BF Elektrotechnik'),(6,'BF Ern&auml;hrung und Hauswirtschaft'),(7,'BF Fahrzeugtechnik'),(8,'BF Farbtechnik und Raumgestaltung'),(9,'BF Gartenbau und Floristik'),(58,'BF Gesundheit'),(10,'BF Holztechnik'),(55,'BF Informatik'),(11,'BF K&ouml;rperpflege'),(12,'BF Medizinisch-technische und krankenpfleger. Berufe'),(13,'BF Metalltechnik'),(14,'BF Neugeordnete Berufe'),(61,'BF Sonstige'),(57,'BF Sozialp&auml;dagogik/Sozialwesen'),(15,'BF Sozialp&auml;gogische Berufe'),(16,'BF Textiltechnik und Bekleidung'),(17,'BF Wirtschaft und Verwaltung'),(18,'Biologie'),(19,'Chemie'),(20,'Darstellendes Spiel'),(21,'Deutsch'),(22,'Deutsch als Fremd- u. Zweitsprache'),(23,'Englisch'),(24,'Ethik'),(25,'F&auml;cher&uuml;bergreifend'),(26,'Franz&ouml;sisch'),(27,'Geographie/Erdkunde'),(28,'Geschichte'),(29,'Gesellschaftslehre'),(30,'Griechisch'),(31,'Hebr&auml;isch'),(32,'Herkunftssprachlicher Unterricht'),(33,'Informatik'),(34,'Italienisch'),(53,'kein Fachbezug'),(35,'Kunst'),(36,'Latein'),(52,'Mathe'),(37,'Mathematik'),(38,'Musik'),(39,'Naturwissenschaften'),(40,'Philosophie'),(41,'Physik'),(42,'Politik u. Wirtschaft'),(43,'Portugiesisch'),(44,'Religion ev.'),(45,'Religion kath.'),(46,'Russisch'),(47,'Sachunterricht'),(48,'Spanisch'),(49,'Sport'),(50,'T&uuml;rkisch'),(51,'Werken/Textiles Gestalten');
/*!40000 ALTER TABLE `dms_fort_fach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_fort_schulart`
--

DROP TABLE IF EXISTS `dms_fort_schulart`;
CREATE TABLE `dms_fort_schulart` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_fort_schulart`
--

LOCK TABLES `dms_fort_schulart` WRITE;
/*!40000 ALTER TABLE `dms_fort_schulart` DISABLE KEYS */;
INSERT INTO `dms_fort_schulart` VALUES (1,'Alle'),(37,'Alle Schulformen'),(20,'Berufliche Schulen'),(24,'F&ouml;rderschule'),(27,'F&ouml;rderschule und Grundschule oder Sekundarstufe I'),(40,'F&ouml;rderschule/Grundschule oder Sek. I'),(36,'F&ouml;rderstufe'),(41,'F&ouml;rderstufe/&Uuml;bergang 5/6'),(25,'Grundschule'),(26,'Grundschule und Sekundarstufe I'),(38,'Gymnasiale Oberst. (inkl. Berufl. Gymn.)'),(21,'Gymnasiale Oberstufe'),(23,'Gymnasium'),(31,'Hauptschule'),(29,'Integrierte Gesamtschule'),(34,'Kooperative Gesamtschule'),(35,'Realschule'),(33,'Schule f&uuml;r Erwachsene'),(39,'Sekundarstufe I'),(32,'Sekundarstufe I ohne Gymnasium'),(22,'Sekundarstufe I, alle Schulformen'),(28,'Teilzeitberufsschule'),(30,'Vollzeitberufsschule'),(42,'Vorklasse/Eingangsstufe');
/*!40000 ALTER TABLE `dms_fort_schulart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_ms_dmsmediasurvey`
--

DROP TABLE IF EXISTS `dms_ms_dmsmediasurvey`;
CREATE TABLE `dms_ms_dmsmediasurvey` (
  `id` int(11) NOT NULL auto_increment,
  `org_id` int(11) NOT NULL,
  `last_modified` datetime NOT NULL,
  `eigene_com` tinyint(1) NOT NULL,
  `raeume_gesamt` int(11) NOT NULL,
  `mit_com_pcraum` int(11) NOT NULL,
  `mit_com_fachraum` int(11) NOT NULL,
  `ohne_com_pcraum` int(11) NOT NULL,
  `ohne_com_fachraum` int(11) NOT NULL,
  `anz_com_pcraum` int(11) NOT NULL,
  `anz_com_fachraum` int(11) NOT NULL,
  `nutzung_sch_com` tinyint(1) NOT NULL,
  `typ_1` int(11) NOT NULL,
  `typ_1_mobil` int(11) NOT NULL,
  `typ_2` int(11) NOT NULL,
  `typ_2_mobil` int(11) NOT NULL,
  `notebook` int(11) NOT NULL,
  `notebook_klasse` int(11) NOT NULL,
  `eigene_plattform` tinyint(1) NOT NULL,
  `netz` tinyint(1) NOT NULL,
  `netz_com` int(11) NOT NULL,
  `netz_wlan` int(11) NOT NULL,
  `netz_raum` int(11) NOT NULL,
  `internet` tinyint(1) NOT NULL,
  `internet_anz` int(11) NOT NULL,
  `nutzung` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_ms_dmsmediasurvey`
--

LOCK TABLES `dms_ms_dmsmediasurvey` WRITE;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_ms_dmsmediasurvey_gruppe`
--

DROP TABLE IF EXISTS `dms_ms_dmsmediasurvey_gruppe`;
CREATE TABLE `dms_ms_dmsmediasurvey_gruppe` (
  `id` int(11) NOT NULL auto_increment,
  `gruppe` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_ms_dmsmediasurvey_gruppe_gruppe` (`gruppe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_ms_dmsmediasurvey_gruppe`
--

LOCK TABLES `dms_ms_dmsmediasurvey_gruppe` WRITE;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_gruppe` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_gruppe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_ms_dmsmediasurvey_gruppe_form`
--

DROP TABLE IF EXISTS `dms_ms_dmsmediasurvey_gruppe_form`;
CREATE TABLE `dms_ms_dmsmediasurvey_gruppe_form` (
  `id` int(11) NOT NULL auto_increment,
  `gruppe_id` int(11) NOT NULL,
  `form` varchar(40) NOT NULL,
  `title` varchar(120) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_ms_dmsmediasurvey_gruppe_form_gruppe_id` (`gruppe_id`),
  KEY `dms_ms_dmsmediasurvey_gruppe_form_form` (`form`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_ms_dmsmediasurvey_gruppe_form`
--

LOCK TABLES `dms_ms_dmsmediasurvey_gruppe_form` WRITE;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_gruppe_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_gruppe_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_ms_dmsmediasurvey_items`
--

DROP TABLE IF EXISTS `dms_ms_dmsmediasurvey_items`;
CREATE TABLE `dms_ms_dmsmediasurvey_items` (
  `id` int(11) NOT NULL auto_increment,
  `gruppe_form_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  `multi` tinyint(1) NOT NULL,
  `org_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_ms_dmsmediasurvey_items_gruppe_form_id` (`gruppe_form_id`),
  KEY `dms_ms_dmsmediasurvey_items_option_id` (`option_id`),
  KEY `dms_ms_dmsmediasurvey_items_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_ms_dmsmediasurvey_items`
--

LOCK TABLES `dms_ms_dmsmediasurvey_items` WRITE;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dms_ms_dmsmediasurvey_option`
--

DROP TABLE IF EXISTS `dms_ms_dmsmediasurvey_option`;
CREATE TABLE `dms_ms_dmsmediasurvey_option` (
  `id` int(11) NOT NULL auto_increment,
  `gruppe_id` int(11) NOT NULL,
  `option` varchar(40) NOT NULL,
  `title` varchar(120) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `dms_ms_dmsmediasurvey_option_option` (`option`),
  KEY `gruppe_id` (`gruppe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dms_ms_dmsmediasurvey_option`
--

LOCK TABLES `dms_ms_dmsmediasurvey_option` WRITE;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_option` DISABLE KEYS */;
/*!40000 ALTER TABLE `dms_ms_dmsmediasurvey_option` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2007-11-29 15:56:47
