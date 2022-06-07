
DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
  id INTEGER NOT NULL PRIMARY KEY,
  firstName VARCHAR(100) NOT NULL,
  lastName VARCHAR(100) NOT NULL,
  personal_id VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  mobile VARCHAR(15) NULL,
  email VARCHAR(50) NULL,
  committeeMember INTEGER NOT NULL
  
);


-- CREATE UNIQUE INDEX uq_mobile
-- ON employee(mobile);

-- CREATE UNIQUE INDEX uq_email
-- ON employee(email);

CREATE UNIQUE INDEX uq_personal_id
ON employee(personal_id);


DROP TABLE IF EXISTS idea;
CREATE TABLE idea (
  id INTEGER  NOT NULL ,
  employeeId INTEGER  NOT NULL,
  categoryId INTEGER  NOT NULL,
  title VARCHAR(200) NOT NULL,
  text TEXT NOT NULL,
  costReduction FLOAT NULL ,
  time DATETIME NOT NULL,
  status TEXT CHECK( status IN ('NotChecked', 'Pending', 'Accepted', 'Rejected', 'Implemented') )  NOT NULL ,
  PRIMARY KEY (id),
  FOREIGN KEY (categoryId) REFERENCES ideaCategory(id),
  FOREIGN KEY (employeeId) REFERENCES employee(id)
);

CREATE INDEX idx_idea_employee
ON idea(employeeId);


DROP TABLE IF EXISTS ideaVote;
CREATE TABLE ideaVote (
  id INTEGER NOT NULL ,
  employeeId INTEGER NOT NULL,
  ideaId INTEGER NOT NULL,
  type INT NOT NULL,
  time DATETIME NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (employeeId) REFERENCES employee(id),
  FOREIGN KEY (ideaId) REFERENCES idea(id)
);


CREATE INDEX idx_vote_idea
ON ideaVote(ideaId);


DROP TABLE IF EXISTS comment;
CREATE TABLE comment (
  id INTEGER NOT NULL ,
  employeeId INTEGER NOT NULL,
  ideaId INTEGER NOT NULL,
  text TEXT NOT NULL,
  time DATETIME NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (employeeId) REFERENCES employee(id),
  FOREIGN KEY (ideaId) REFERENCES idea(id)
);


CREATE INDEX idx_comment_idea
ON comment(ideaId);


DROP TABLE IF EXISTS commentVote;
CREATE TABLE commentVote (
  id INTEGER NOT NULL ,
  employeeId INTEGER  NOT NULL,
  commentId  INTEGER  NOT NULL,
  type INT NOT NULL,
  time DATETIME NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (employeeId) REFERENCES employee(id),
  FOREIGN KEY (commentId) REFERENCES comment(id)
);

CREATE INDEX idx_vote_comment
ON commentVote(commentId);


DROP TABLE IF EXISTS award;
CREATE TABLE award (
  id INTEGER NOT NULL ,
  employeeId INTEGER NOT NULL,
  ideaId INTEGER NOT NULL,
  value FLOAT NOT NULL ,
  time DATETIME NOT NULL,
  type TEXT CHECK( type IN ('committee','lottery') )NOT NULL ,
  PRIMARY KEY (id),
  FOREIGN KEY (employeeId) REFERENCES employee(id),
  FOREIGN KEY (ideaId) REFERENCES idea(id)
);

CREATE INDEX idx_award_employeeIdea
ON award(employeeId);


DROP TABLE IF EXISTS committeeScoreHeader;
CREATE TABLE committeeScoreHeader (
  id INTEGER NOT NULL ,
  employeeId INTEGER NOT NULL,
  ideaId INTEGER NOT NULL,
  time DATETIME NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (employeeId) REFERENCES employee(id),
  FOREIGN KEY (ideaId) REFERENCES idea(id)
);



DROP TABLE IF EXISTS evaluationCriteria;
CREATE TABLE evaluationCriteria (
  id INTEGER NOT NULL PRIMARY KEY,
  title TEXT NOT NULL,
  weight FLOAT NOT NULL 
);

DROP TABLE IF EXISTS ideaCategory;
CREATE TABLE ideaCategory (
  id INTEGER NOT NULL PRIMARY KEY ,
  title TEXT NOT NULL
  
);



DROP TABLE IF EXISTS committeeScoreDetail;
CREATE TABLE committeeScoreDetail (
  id INTEGER NOT NULL PRIMARY KEY  ,
  committeeScoreHeaderId INTEGER NOT NULL,
  evaluationCriteriaId INTEGER NOT NULL,
  score  INTEGER NOT NULL,
  FOREIGN KEY (committeeScoreHeaderId) REFERENCES committeeScoreHeader(id),
  FOREIGN KEY (evaluationCriteriaId) REFERENCES evaluationCriteria(id)
);
