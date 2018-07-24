/*
Navicat MySQL Data Transfer

Source Server         : 172.20.78.96
Source Server Version : 50720
Source Host           : 172.20.78.96:3306
Source Database       : testdb

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-07-24 18:01:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES ('1', 'python1班');
INSERT INTO `class` VALUES ('2', 'java2班');
INSERT INTO `class` VALUES ('3', 'C语言3班');

-- ----------------------------
-- Table structure for course_record
-- ----------------------------
DROP TABLE IF EXISTS `course_record`;
CREATE TABLE `course_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `course_record_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`),
  CONSTRAINT `course_record_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of course_record
-- ----------------------------
INSERT INTO `course_record` VALUES ('2', '2018-07-16 16:23:03', '2', '1', '课程1，作业：计算1+1');

-- ----------------------------
-- Table structure for homework
-- ----------------------------
DROP TABLE IF EXISTS `homework`;
CREATE TABLE `homework` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `homework_path` varchar(100) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `record_id` (`record_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `homework_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `course_record` (`id`),
  CONSTRAINT `homework_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of homework
-- ----------------------------
INSERT INTO `homework` VALUES ('1', null, '2', '3', null);
INSERT INTO `homework` VALUES ('2', null, '2', '4', null);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', 'student');
INSERT INTO `role` VALUES ('2', 'teacher');
INSERT INTO `role` VALUES ('3', 'manager');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `account` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `qq` varchar(50) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'admin', 'admin', 'admin', '10000', '3');
INSERT INTO `user` VALUES ('2', 'alex', 'alex', '123456', '329280192', '2');
INSERT INTO `user` VALUES ('3', 'zhangsan', 'zhangsan', '123456', '329287399', '1');
INSERT INTO `user` VALUES ('4', 'lisi', 'lisi', '123456', '39947747', '1');

-- ----------------------------
-- Table structure for user_m2m_class
-- ----------------------------
DROP TABLE IF EXISTS `user_m2m_class`;
CREATE TABLE `user_m2m_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `class_id` (`class_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_m2m_class_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`),
  CONSTRAINT `user_m2m_class_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_m2m_class
-- ----------------------------
INSERT INTO `user_m2m_class` VALUES ('1', '1', '3');
INSERT INTO `user_m2m_class` VALUES ('2', '1', '4');
INSERT INTO `user_m2m_class` VALUES ('3', '2', '4');
INSERT INTO `user_m2m_class` VALUES ('4', '3', '4');
INSERT INTO `user_m2m_class` VALUES ('5', '2', '3');
INSERT INTO `user_m2m_class` VALUES ('6', '3', '3');
SET FOREIGN_KEY_CHECKS=1;
