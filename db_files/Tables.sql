
CREATE DATABASE IdeaManagementSystem;
USE IdeaManagementSystem;

DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(100) NOT NULL,
  `lastName` VARCHAR(100) NOT NULL,
  `personal_id` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `mobile` VARCHAR(15) NULL,
  `email` VARCHAR(50) NULL,
  `committeeMember` BOOL NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_mobile` (`mobile`),
  UNIQUE INDEX `uq_email` (`email`),
  UNIQUE INDEX `uq_personal_id` (`personal_id`)
);



DROP TABLE IF EXISTS `idea`;
CREATE TABLE `idea` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `categoryId` INT UNSIGNED NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  `costReduction` FLOAT NULL ,
  `time` DATETIME NOT NULL,
  `status` ENUM( 'NotChecked','Pending' , 'Accepted' , 'Rejected' , 'Implemented' ) NOT NULL ,
  PRIMARY KEY (`id`),
  INDEX `idx_idea_employee` (`employeeId`),
  FOREIGN KEY (`categoryId`) REFERENCES `ideaCategory`(`id`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`)
);


DROP TABLE IF EXISTS `ideaVote`;
CREATE TABLE `ideaVote` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `ideaId` INT UNSIGNED NOT NULL,
  `type` BOOL NOT NULL,
  `time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_vote_idea` (`ideaId`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`),
  FOREIGN KEY (`ideaId`) REFERENCES `idea`(`id`)
);




DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `ideaId` INT UNSIGNED NOT NULL,
  `text` TINYTEXT NOT NULL,
  `time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_comment_idea` (`ideaId`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`),
  FOREIGN KEY (`ideaId`) REFERENCES `idea`(`id`)
);


DROP TABLE IF EXISTS `commentVote`;
CREATE TABLE `commentVote` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `commentId`  INT UNSIGNED NOT NULL,
  `type` BOOL NOT NULL,
  `time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_vote_comment` (`commentId`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`),
  FOREIGN KEY (`commentId`) REFERENCES `comment`(`id`)
);


DROP TABLE IF EXISTS `award`;
CREATE TABLE `award` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `ideaId` INT UNSIGNED NOT NULL,
  `value` FLOAT NOT NULL ,
  `time` DATETIME NOT NULL,
  `type` ENUM( 'committee','lottery' ) NOT NULL ,
  PRIMARY KEY (`id`),
  INDEX `idx_award_employeeIdea` (`employeeId`, `ideaId`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`),
  FOREIGN KEY (`ideaId`) REFERENCES `idea`(`id`)
);


DROP TABLE IF EXISTS `committeeScoreHeader`;
CREATE TABLE `committeeScoreHeader` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `employeeId` INT UNSIGNED NOT NULL,
  `ideaId` INT UNSIGNED NOT NULL,
  `time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_score_idea` (`ideaId`),
  FOREIGN KEY (`employeeId`) REFERENCES `employee`(`id`),
  FOREIGN KEY (`ideaId`) REFERENCES `idea`(`id`)
);



DROP TABLE IF EXISTS `evaluationCriteria`;
CREATE TABLE `evaluationCriteria` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `weight` FLOAT NOT NULL ,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `ideaCategory`;
CREATE TABLE `ideaCategory` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`)
);



DROP TABLE IF EXISTS `committeeScoreDetail`;
CREATE TABLE `committeeScoreDetail` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `committeeScoreHeaderId` INT UNSIGNED NOT NULL,
  `evaluationCriteriaId` INT UNSIGNED NOT NULL,
  `score`  INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`committeeScoreHeaderId`) REFERENCES `committeeScoreHeader`(`id`),
  FOREIGN KEY (`evaluationCriteriaId`) REFERENCES `evaluationCriteria`(`id`)
);