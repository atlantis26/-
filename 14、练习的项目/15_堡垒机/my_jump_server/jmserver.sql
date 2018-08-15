/*
Navicat MySQL Data Transfer

Source Server         : 172.20.78.96
Source Server Version : 50720
Source Host           : 172.20.78.96:3306
Source Database       : jmserver

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-08-15 17:48:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for audit_log
-- ----------------------------
DROP TABLE IF EXISTS `audit_log`;
CREATE TABLE `audit_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `bind_host_id` int(11) DEFAULT NULL,
  `action_type` varchar(255) DEFAULT NULL,
  `cmd` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `bind_host_id` (`bind_host_id`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `audit_log_ibfk_2` FOREIGN KEY (`bind_host_id`) REFERENCES `bind_host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_log
-- ----------------------------

-- ----------------------------
-- Table structure for bind_host
-- ----------------------------
DROP TABLE IF EXISTS `bind_host`;
CREATE TABLE `bind_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) DEFAULT NULL,
  `remoteuser_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_bindhost_and_user_uc` (`host_id`,`remoteuser_id`),
  KEY `remoteuser_id` (`remoteuser_id`),
  CONSTRAINT `bind_host_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`),
  CONSTRAINT `bind_host_ibfk_2` FOREIGN KEY (`remoteuser_id`) REFERENCES `remote_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bind_host
-- ----------------------------
INSERT INTO `bind_host` VALUES ('2', '1', '2');
INSERT INTO `bind_host` VALUES ('1', '1', '3');
INSERT INTO `bind_host` VALUES ('3', '2', '2');

-- ----------------------------
-- Table structure for bindhost_2_group
-- ----------------------------
DROP TABLE IF EXISTS `bindhost_2_group`;
CREATE TABLE `bindhost_2_group` (
  `bindhost_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`bindhost_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `bindhost_2_group_ibfk_1` FOREIGN KEY (`bindhost_id`) REFERENCES `bind_host` (`id`),
  CONSTRAINT `bindhost_2_group_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bindhost_2_group
-- ----------------------------
INSERT INTO `bindhost_2_group` VALUES ('1', '1');
INSERT INTO `bindhost_2_group` VALUES ('2', '1');
INSERT INTO `bindhost_2_group` VALUES ('3', '1');

-- ----------------------------
-- Table structure for bindhost_2_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `bindhost_2_userprofile`;
CREATE TABLE `bindhost_2_userprofile` (
  `bindhost_id` int(11) NOT NULL,
  `uerprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`bindhost_id`,`uerprofile_id`),
  KEY `uerprofile_id` (`uerprofile_id`),
  CONSTRAINT `bindhost_2_userprofile_ibfk_1` FOREIGN KEY (`bindhost_id`) REFERENCES `bind_host` (`id`),
  CONSTRAINT `bindhost_2_userprofile_ibfk_2` FOREIGN KEY (`uerprofile_id`) REFERENCES `user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bindhost_2_userprofile
-- ----------------------------
INSERT INTO `bindhost_2_userprofile` VALUES ('2', '2');
INSERT INTO `bindhost_2_userprofile` VALUES ('1', '4');
INSERT INTO `bindhost_2_userprofile` VALUES ('2', '4');
INSERT INTO `bindhost_2_userprofile` VALUES ('3', '4');

-- ----------------------------
-- Table structure for group
-- ----------------------------
DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of group
-- ----------------------------
INSERT INTO `group` VALUES ('1', 'web_devteam');

-- ----------------------------
-- Table structure for group_2_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `group_2_userprofile`;
CREATE TABLE `group_2_userprofile` (
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`userprofile_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `group_2_userprofile_ibfk_1` FOREIGN KEY (`userprofile_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `group_2_userprofile_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of group_2_userprofile
-- ----------------------------
INSERT INTO `group_2_userprofile` VALUES ('1', '1');
INSERT INTO `group_2_userprofile` VALUES ('2', '1');
INSERT INTO `group_2_userprofile` VALUES ('3', '1');
INSERT INTO `group_2_userprofile` VALUES ('4', '1');

-- ----------------------------
-- Table structure for host
-- ----------------------------
DROP TABLE IF EXISTS `host`;
CREATE TABLE `host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(64) NOT NULL,
  `ip_addr` varchar(128) NOT NULL,
  `port` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `ip_addr` (`ip_addr`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host
-- ----------------------------
INSERT INTO `host` VALUES ('1', 'test_server1', '172.20.78.97', '22');
INSERT INTO `host` VALUES ('2', 'test_server2', '172.20.78.99', '22');

-- ----------------------------
-- Table structure for remote_user
-- ----------------------------
DROP TABLE IF EXISTS `remote_user`;
CREATE TABLE `remote_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auth_type` varchar(255) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_user_passwd_uc` (`auth_type`,`username`,`password`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of remote_user
-- ----------------------------
INSERT INTO `remote_user` VALUES ('3', 'ssh-key', 'root', null);
INSERT INTO `remote_user` VALUES ('1', 'ssh-passwd', 'root', '123456');
INSERT INTO `remote_user` VALUES ('2', 'ssh-passwd', 'test1', '123456');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', 'manager');
INSERT INTO `role` VALUES ('2', 'user');

-- ----------------------------
-- Table structure for user_profile
-- ----------------------------
DROP TABLE IF EXISTS `user_profile`;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `password` (`password`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_profile_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_profile
-- ----------------------------
INSERT INTO `user_profile` VALUES ('1', 'admin', 'admin', '1');
INSERT INTO `user_profile` VALUES ('2', 'alex', 'alex123', '2');
INSERT INTO `user_profile` VALUES ('3', 'jack', 'jack123', '2');
INSERT INTO `user_profile` VALUES ('4', 'test1', '123456', '2');
SET FOREIGN_KEY_CHECKS=1;
