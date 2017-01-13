 CREATE TABLE `bookinformation` (
  `number` tinyint(4) NOT NULL AUTO_INCREMENT,
  `bookname` char(50) DEFAULT NULL,
  `latestchapter` char(100) DEFAULT NULL,
  `bookmark` char(100) DEFAULT NULL,
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `url` tinytext,
  `ts` datetime DEFAULT CURRENT_TIMESTAMP,
  `dr` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`number`),
  UNIQUE KEY `bookname` (`bookname`)
ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8

create trigger upts before update on bookinformation
for each row
set new.ts=now()
