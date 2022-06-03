DROP DATABASE IF EXISTS db_datawarehousing;
CREATE DATABASE db_datawarehousing;

USE db_datawarehousing;
USE db_annp

CREATE TABLE db_datawarehousing.swimstyle(
    swimstyleid     INT NOT NULL,
    distance        VARCHAR(25),
    stroke          VARCHAR(25),
    relaycount      VARCHAR(25),

    PRIMARY KEY(swimstyleid) 
);


CREATE TABLE db_datawarehousing.club(
    clubid          INT NOT NULL,
    code            VARCHAR(25),
    name            VARCHAR(50),
    nation          VARCHAR(25),
    region          VARCHAR(25),
    PRIMARY KEY(clubid) 
);


CREATE TABLE db_datawarehousing.athlete(
    athleteid       INT NOT NULL,
    completeName    VARCHAR(50),
    nation          VARCHAR(25),
    birthdate       VARCHAR(25),
    license         VARCHAR(25),
    gender          VARCHAR(25),

    PRIMARY KEY(athleteid) 
);

CREATE TABLE db_datawarehousing.meet(
    meetid          INT NOT NULL,
    city            VARCHAR(25),
    name            VARCHAR(75),
    organizer       VARCHAR(50),  
    number          VARCHAR(25),
    dateStart       VARCHAR(25), /*vem do session */            
    dateEnd         VARCHAR(25), /*vem do session */
    course          VARCHAR(25), 
    PRIMARY KEY(meetid) 
);

INSERT INTO db_datawarehousing.swimstyle(swimstyleid, distance, stroke, relaycount) 
    SELECT swimstyleid, distance, stroke, relaycount FROM db_annp.swimstyle;

INSERT INTO db_datawarehousing.club(clubid, code, name, nation, region) 
    SELECT clubid, code, name, nation, region FROM db_annp.club;

INSERT INTO db_datawarehousing.athlete(athleteid, completeName, nation, birthdate, license,gender) 
    SELECT athleteid, concat(firstname, ' ', lastname) as name, nation, birthdate , license, gender FROM db_annp.athlete;

INSERT INTO db_datawarehousing.meet(meetid, city, name, organizer, number, course)
    SELECT meetid, city, name, organizer, number, course FROM db_annp.meet;

/* TODO: Preencher depois
INSERT INTO db_datawarehousing.meet(meetid, dateStart, dateEnd) 
    SELECT db_annp.meet.meetid, MIN(date), MAX(date) FROM db_annp.session, db_annp.meet where db_datawarehousing.meet.meetid = db_annp.session.meetid GROUP BY db_annp.session.meetid;*/

CREATE TABLE db_datawarehousing.fact(
    athleteid   INT,    
    swimstyleid INT,   
    clubid      INT,   
    meetid      INT,   
    
    swimTime    VARCHAR(25), /*Vem do result*/
    points      VARCHAR(25), /*Vem do result*/
    poolName    VARCHAR(50),

    FOREIGN KEY (athleteid) REFERENCES db_datawarehousing.athlete(athleteid),
    FOREIGN KEY (swimstyleid) REFERENCES db_datawarehousing.swimstyle(swimstyleid),
    FOREIGN KEY (clubid) REFERENCES db_datawarehousing.club(clubid),
    FOREIGN KEY (meetid) REFERENCES db_datawarehousing.meet(meetid)
);

INSERT INTO db_datawarehousing.fact(athleteid, clubid) 
    SELECT athlete.athleteid, club.clubid FROM db_annp.athlete, db_annp.club WHERE athlete.clubid = club.clubid;

INSERT INTO db_datawarehousing.fact(points, swimTime)
    SELECT result.points, result.swimTime FROM db_annp.result WHERE db_annp.result.resultid = db_datawarehousing.athlete.athleteid
