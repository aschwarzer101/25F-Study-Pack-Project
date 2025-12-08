DROP DATABASE IF EXISTS `StudyPack`;
CREATE DATABASE IF NOT EXISTS `StudyPack`;


USE `StudyPack`;


DROP TABLE IF EXISTS Professor;
CREATE TABLE Professor
(
   firstName  varchar(50)     not null,
   lastName   varchar(50)     not null,
   department varchar(100)    not null,
   degree1    varchar(75)     not null,
   degree2    varchar(75)     not null,
   degree3    varchar(75)     not null,
   profId     int PRIMARY KEY not null
);
DROP TABLE IF EXISTS Course;
CREATE TABLE Course
(
   crn        INT PRIMARY KEY,
   department VARCHAR(255) NOT NULL,
   courseNum  INT          NOT NULL,
   name       VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS Professor_Course;
CREATE TABLE Professor_Course
(
   profID int,
   CRN    int,
   primary key (profID, CRN),
   FOREIGN KEY (profID) REFERENCES Professor (profID),
   FOREIGN KEY (CRN) REFERENCES Course (CRN)
);


DROP TABLE IF EXISTS `TA_Admin`;
CREATE TABLE `TA_Admin`
(
   nuID      INT PRIMARY KEY,
   firstName VARCHAR(255) NOT NULL,
   lastName  VARCHAR(255) NOT NULL,
   email     VARCHAR(255) UNIQUE,
   crn       INT          NOT NULL,
   FOREIGN KEY (crn) REFERENCES Course (crn)
);


DROP TABLE IF EXISTS TeachingAssistant;
CREATE TABLE TeachingAssistant
(
   nuID      INT PRIMARY KEY,
   firstName VARCHAR(255)        NOT NULL,
   lastName  VARCHAR(255)        NOT NULL,
   email     VARCHAR(255) UNIQUE NOT NULL,
   crn       INT                 NOT NULL,
   adminID   INT                 NOT NULL,
   FOREIGN KEY (adminID) REFERENCES TA_Admin (nuID),
   FOREIGN KEY (crn) REFERENCES Course (crn)
);


drop table if exists Student;
CREATE TABLE Student
(
   nuID      INT PRIMARY KEY,
   firstName VARCHAR(255)        NOT NULL,
   lastName  VARCHAR(255)        NOT NULL,
   email     VARCHAR(255) UNIQUE NOT NULL,
   gradYear  DATETIME            NOT NULL,
   classYear INT DEFAULT (5 - (YEAR(gradYear) - YEAR(CURRENT_DATE))),
   majorOne  VARCHAR(255)        NOT NULL,
   majorTwo  VARCHAR(255),
   minor     VARCHAR(255)


);


drop table if exists EnrolledIn;
create table EnrolledIn
(
   nuID       int         not null,
   CRN        int         not null,
   year       int         not null,
   semester   varchar(15) not null,
   sectionNum int         not null,
   primary key (nuID, CRN),
   foreign key (nuID) references Student (nuID),
   foreign key (CRN) references Course (CRN)
);


drop table if exists ProjectGroup;
create table ProjectGroup
(
   teamID   int not null,
   CRN      int not null,
   teamName varchar(50),
   primary key (teamID, CRN),
   foreign key (CRN) references Course (CRN)
);


drop table if exists ProjectGroup_Student;
create table ProjectGroup_Student
(
   nuID      int         not null,
   teamID    int         not null,
   CRN       INT         NOT NULL,
   firstName varchar(50) not null,
   lastName  varchar(50) not null,
   primary key (nuID, teamID),
   foreign key (nuID) references Student (nuID),
   foreign key (teamID, CRN) references ProjectGroup (teamID, CRN)
);


drop table if exists Resource;
create table Resource
(
   resourceID   int                                                        not null PRIMARY KEY AUTO_INCREMENT,
   name         varchar(100)                                               not null,
   type         ENUM ('PDF', 'Textbook', 'Video', 'URL', 'Image', 'Other') not null,
   dateUploaded DATE                                                       not null,
   description  varchar(200),
   CRN          int,
   profID       int,
   foreign key (CRN) references Course (CRN),
   foreign key (profID) references Professor (profID)
);


DROP TABLE IF EXISTS SessionRequest;
CREATE TABLE SessionRequest
(
   requestID   INT PRIMARY KEY AUTO_INCREMENT,
   status      VARCHAR(255) NOT NULL,
   dateCreated DATE         NOT NULL,
   adminID     INT          NOT NULL,
   FOREIGN KEY (adminID) REFERENCES TA_Admin (nuID)
);


DROP TABLE IF EXISTS Requesting_Students;
CREATE TABLE Requesting_Students
(
   requestID INT NOT NULL,
   nuID      INT NOT NULL,


   FOREIGN KEY (requestID) REFERENCES SessionRequest (requestID),
   FOREIGN KEY (nuID) REFERENCES Student (nuID),
   PRIMARY KEY (requestID, nuID)
);


DROP TABLE IF EXISTS StudyLocation;
CREATE TABLE StudyLocation
(
   locID    INT PRIMARY KEY AUTO_INCREMENT,
   status   TINYINT(1) DEFAULT 1,
   capacity INT          NOT NULL,
   room     VARCHAR(255) NOT NULL,
   building VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS TA_Uploads_Resource;
CREATE TABLE TA_Uploads_Resource
(
   resourceID INT NOT NULL AUTO_INCREMENT,
   taID       INT NOT NULL,


   FOREIGN KEY (resourceID) REFERENCES Resource (resourceID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (taID) REFERENCES TeachingAssistant (nuID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   PRIMARY KEY (resourceID, taID)
);


DROP TABLE IF EXISTS StudySession;
CREATE TABLE StudySession
(
   sessionID INT PRIMARY KEY,
   locID     INT       NOT NULL,
   startTime TIMESTAMP NOT NULL,
   endTime   TIMESTAMP NOT NULL,
   date      DATE      NOT NULL,
   adminID   INT,
   studentID INT,
   FOREIGN KEY (adminID) REFERENCES TA_Admin (nuID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (locID) REFERENCES StudyLocation (locID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


DROP TABLE IF EXISTS TA_Attends_Session;
CREATE TABLE TA_Attends_Session
(
   taID      INT NOT NULL,
   sessionID INT NOT NULL,


   FOREIGN KEY (taID) REFERENCES TeachingAssistant (nuID),
   FOREIGN KEY (sessionID) REFERENCES StudySession (sessionID),
   PRIMARY KEY (taID, sessionID)
);


DROP TABLE IF EXISTS Topic;
CREATE TABLE Topic
(
   crn     INT          NOT NULL,
   topicID INT          NOT NULL,
   name    VARCHAR(255) NOT NULL,


   FOREIGN KEY (crn) REFERENCES Course (crn),
   PRIMARY KEY (crn, topicID)
);


DROP TABLE IF EXISTS Session_Covers_Topic;
CREATE TABLE Session_Covers_Topic
(
   crn       INT NOT NULL,
   topicID   INT,
   sessionID INT,
   FOREIGN KEY (crn, topicID) REFERENCES Topic (crn, topicID),
   FOREIGN KEY (sessionID) REFERENCES StudySession (sessionID),
   PRIMARY KEY (topicID, sessionID)
);


DROP TABLE IF EXISTS Announcement;
CREATE TABLE Announcement
(
   ancmID     INT PRIMARY KEY AUTO_INCREMENT,
   title      VARCHAR(255) NOT NULL,
   datePosted DATE         NOT NULL,
   text       TEXT         NOT NULL,
   adminID    INT          NOT NULL,


   FOREIGN KEY (adminID) REFERENCES TA_Admin (nuID)
);


DROP TABLE IF EXISTS Tag;
CREATE TABLE Tag
(
   tagID             INT PRIMARY KEY AUTO_INCREMENT,
   tagName           VARCHAR(255) NOT NULL,
   `studentCreated?` TINYINT(1) DEFAULT 0
);


DROP TABLE IF EXISTS Request_Tags;
CREATE TABLE Request_Tags
(
   tagID     INT NOT NULL,
   requestID INT NOT NULL,


   FOREIGN KEY (tagID) REFERENCES Tag (tagID),
   FOREIGN KEY (requestID) REFERENCES SessionRequest (requestID),
   PRIMARY KEY (tagID, requestID)
);


DROP TABLE IF EXISTS Student_Uploads_Resource;
CREATE TABLE Student_Uploads_Resource
(
   resourceID INT NOT NULL AUTO_INCREMENT,
   studentID  INT NOT NULL,
   FOREIGN KEY (resourceID) REFERENCES Resource (resourceID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (studentID) REFERENCES Student (nuID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   PRIMARY KEY (resourceID, studentID)
);


DROP TABLE IF EXISTS Student_Joins_Session;
CREATE TABLE Student_Joins_Session
(


   nuID      INT NOT NULL,
   sessionID INT NOT NULL,
   FOREIGN KEY (nuID) REFERENCES Student (nuID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,
   FOREIGN KEY (sessionID) REFERENCES StudySession (sessionID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,
   PRIMARY KEY (nuID, sessionID)
);


DROP TABLE IF EXISTS PeerTutor;
CREATE TABLE PeerTutor
(
   nuID      INT PRIMARY KEY,
   firstName VARCHAR(255) NOT NULL,
   lastName  VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS PeerTutors_Student;
CREATE TABLE PeerTutors_Student
(
   nuID    INT NOT NULL,
   tutorID INT NOT NULL,
   FOREIGN KEY (nuID) REFERENCES Student (nuID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (tutorID) REFERENCES PeerTutor (nuID),
   PRIMARY KEY (nuID, tutorID)
);


DROP TABLE IF EXISTS Tutor_Aides;
CREATE TABLE Tutor_Aides
(
   tutorID   INT NOT NULL,
   sessionID INT NOT NULL,


   FOREIGN KEY (tutorID) REFERENCES PeerTutor (nuID)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   FOREIGN KEY (sessionID) REFERENCES StudySession (sessionID)
       ON DELETE CASCADE
       ON UPDATE CASCADE,
   PRIMARY KEY (tutorID, sessionID)
);
