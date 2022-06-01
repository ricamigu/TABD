DROP DATABASE IF EXISTS db_datawarehousing;
CREATE DATABASE db_datawarehousing;

USE db_datawarehousing;
USE db_annp

CREATE TABLE db_datawarehousing.result(
    resultid        INT NOT NULL,
    points          VARCHAR(25),
    swimTime        VARCHAR(25),
    reactionTime    VARCHAR(25),
    status          VARCHAR(25),
    /**EventId ??*/
   
    PRIMARY KEY (resultid) 
);

CREATE TABLE db_datawarehousing.split(
    splitid         INT NOT NULL,
    distance        VARCHAR(25),
    swimTime        VARCHAR(25),
    /*ResultId ??*/
    
    PRIMARY KEY (splitid) 
);

CREATE TABLE db_datawarehousing.swimstyle(
    swimstyleid     INT NOT NULL,
    distance        VARCHAR(25),
    stroke          VARCHAR(25),
    relaycount      VARCHAR(25),
    /*EventId???*/
    PRIMARY KEY (swimstyleid) 
);

CREATE TABLE db_datawarehousing.event(
    eventid         INT NOT NULL,
    daytime         VARCHAR(25),
    gender          VARCHAR(25),
    `order`         VARCHAR(25),
    number          VARCHAR(25),
    /*SessionId??*/
    PRIMARY KEY (eventid) 
);

CREATE TABLE db_datawarehousing.club(
    clubid          INT NOT NULL,
    code            VARCHAR(25),
    name            VARCHAR(50),
    nation          VARCHAR(25),
    region          VARCHAR(25),
    /*MeetId??*/
    PRIMARY KEY (clubid) 
);

CREATE TABLE db_datawarehousing.session(
    sessionid       INT NOT NULL,
    date            VARCHAR(25),
    name            VARCHAR(25),
    number          VARCHAR(25),
    warmUpTime      VARCHAR(25),
    /*MeetId*/
    PRIMARY KEY (sessionid) 
);

CREATE TABLE db_datawarehousing.athlete(
    athleteid       INT NOT NULL,
    completeName    VARCHAR(50),
    nation          VARCHAR(25),
    age             INT,
    license         VARCHAR(25),
    /*....*/
    PRIMARY KEY (athleteid) 
);

CREATE TABLE db_datawarehousing.meet(
    meetid          INT NOT NULL,
    city            VARCHAR(25),
    /*
    name            VARCHAR(25),
    organizer       VARCHAR(50),  
    number          VARCHAR(25),
    */
    PRIMARY KEY (meetid) 
);

CREATE TABLE db_datawarehousing.pool(
    poolid          INT NOT NULL,
    /*.Sempre é preciso?.*/
    PRIMARY KEY (poolid) 
);



INSERT INTO db_datawarehousing.result(resultid, points, swimTime, reactionTime, status) 
    SELECT resultid, points, swimTime, reactionTime, status FROM db_annp.result;

INSERT INTO db_datawarehousing.split(splitid, distance, swimTime) 
    SELECT splitid, distance, swimTime FROM db_annp.split;

INSERT INTO db_datawarehousing.swimstyle(swimstyleid, distance, stroke, relaycount) 
    SELECT swimstyleid, distance, stroke, relaycount FROM db_annp.swimstyle;

INSERT INTO db_datawarehousing.event(eventid, daytime, gender, `order`, number) 
    SELECT eventid, daytime, gender, `order`, number FROM db_annp.event;

INSERT INTO db_datawarehousing.club(clubid, code, name, nation, region) 
    SELECT clubid, code, name, nation, region FROM db_annp.club;

INSERT INTO db_datawarehousing.session(sessionid, date, name, number, warmUpTime) 
    SELECT sessionid, date, name, number, timestampdiff(minute, timestamp(date,warmupfrom), timestamp(date,warmupuntil)) as warmUpTime FROM db_annp.session;    /*TODO Mudar o warmUp nesta linha*/

INSERT INTO db_datawarehousing.athlete(athleteid, completeName, nation, age, license) 
    SELECT athleteid,  concat(firstname, ' ', lastname) as name, nation, year(from_days(to_days(now())-to_days(birthdate))) as age , license FROM db_annp.athlete;

INSERT INTO db_datawarehousing.meet(meetid,city) /*TODO Confirmar se é suposto acrescentar mais coisas*/
    SELECT meetid, city FROM db_annp.meet;

INSERT INTO db_datawarehousing.pool(poolid) /*TODO Confirmar se é suposto acrescentar mais coisas*/
    SELECT poolid FROM db_annp.pool;




CREATE TABLE db_datawarehousing.fact(
    resultid    INT,   
    splitid     INT,   
    swimstyleid INT,   
    eventid     INT,    
    clubid      INT,   
    sessionid   INT,    
    athleteid   INT,    
    meetid      INT,   
    poolid      INT,
    factid      INT NOT NULL AUTO_INCREMENT,
    /*Acrescentar mais cenas*/

    /*É necessário primary key??? Acho que sim...*/
    PRIMARY KEY(factid)

    /*FOREIGN KEY (resultid) REFERENCES db_datawarehousing.result(resultid),
    FOREIGN KEY (splitid) REFERENCES db_datawarehousing.split(splitid),
    FOREIGN KEY (swimstyleid) REFERENCES db_datawarehousing.swimstyle(swimstyleid),
    FOREIGN KEY (eventid) REFERENCES db_datawarehousing.event(eventid),
    FOREIGN KEY (clubid) REFERENCES db_datawarehousing.club(clubid),
    FOREIGN KEY (sessionid) REFERENCES db_datawarehousing.session(sessionid),
    FOREIGN KEY (athleteid) REFERENCES db_datawarehousing.athlete(athleteid),
    FOREIGN KEY (meetid) REFERENCES db_datawarehousing.meet(meetid),
    FOREIGN KEY (poolid) REFERENCES db_datawarehousing.pool(poolid)*/
);



INSERT INTO db_datawarehousing.fact(splitid) 
    SELECT splitid FROM db_annp.split;
