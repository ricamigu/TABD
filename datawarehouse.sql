USE db_annp

DROP DATABASE IF EXISTS db_datawarehousing;
CREATE DATABASE db_datawarehousing;

USE db_datawarehousing;

CREATE TABLE db_datawarehousing.result(
    resultid    INT NOT NULL,
    points      VARCHAR(25),
    /*....*/
    PRIMARY KEY (resultid) 
);

CREATE TABLE db_datawarehousing.split(
    splitid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (splitid) 
);

CREATE TABLE db_datawarehousing.swimstyle(
    swimstyleid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (swimstyleid) 
);

CREATE TABLE db_datawarehousing.event(
    eventid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (eventid) 
);

CREATE TABLE db_datawarehousing.club(
    clubid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (clubid) 
);

CREATE TABLE db_datawarehousing.session(
    sessionid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (sessionid) 
);

CREATE TABLE db_datawarehousing.athelete(
    atheleteid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (atheleteid) 
);

CREATE TABLE db_datawarehousing.meet(
    meetid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (meetid) 
);

CREATE TABLE db_datawarehousing.pool(
    poolid    INT NOT NULL,
    /*....*/
    PRIMARY KEY (poolid) 
);



INSERT INTO db_datawarehousing.result(resultid,points) 
    SELECT resultid, points FROM db_annp.result;

INSERT INTO db_datawarehousing.split(splitid) 
    SELECT splitid FROM db_annp.split;

INSERT INTO db_datawarehousing.swimstyle(swimstyleid) 
    SELECT swimstyleid FROM db_annp.swimstyle;

INSERT INTO db_datawarehousing.event(eventid) 
    SELECT eventid FROM db_annp.event;

INSERT INTO db_datawarehousing.club(clubid) 
    SELECT clubid FROM db_annp.club;

INSERT INTO db_datawarehousing.session(sessionid) 
    SELECT sessionid FROM db_annp.session;

INSERT INTO db_datawarehousing.athelete(atheleteid) 
    SELECT sessionid FROM db_annp.session;

INSERT INTO db_datawarehousing.meet(meetid) 
    SELECT meetid FROM db_annp.meet;

INSERT INTO db_datawarehousing.pool(poolid) 
    SELECT poolid FROM db_annp.pool;




CREATE TABLE db_datawarehousing.fact(
    resultid    INT,   
    splitid     INT,   
    swimstyleid INT,   
    eventid     INT,    
    clubid      INT,   
    sessionid   INT,    
    atheleteid  INT,    
    meetid      INT,   
    poolid      INT,
    factid      INT NOT NULL AUTO_INCREMENT,
    /*Acrescentar mais cenas*/

    /*É necessário primary key??? Acho que sim...*/
    PRIMARY KEY(factid),

    FOREIGN KEY (resultid) REFERENCES db_datawarehousing.result(resultid),
    FOREIGN KEY (splitid) REFERENCES db_datawarehousing.split(splitid),
    FOREIGN KEY (swimstyleid) REFERENCES db_datawarehousing.swimstyle(swimstyleid),
    FOREIGN KEY (eventid) REFERENCES db_datawarehousing.event(eventid),
    FOREIGN KEY (clubid) REFERENCES db_datawarehousing.club(clubid),
    FOREIGN KEY (sessionid) REFERENCES db_datawarehousing.session(sessionid),
    FOREIGN KEY (atheleteid) REFERENCES db_datawarehousing.athelete(atheleteid),
    FOREIGN KEY (meetid) REFERENCES db_datawarehousing.meet(meetid),
    FOREIGN KEY (poolid) REFERENCES db_datawarehousing.pool(poolid)
);


INSERT INTO db_datawarehousing.fact(splitid) 
    SELECT splitid FROM db_annp.split;
