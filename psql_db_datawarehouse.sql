DROP TABLE IF EXISTS swimstyle CASCADE;
DROP TABLE IF EXISTS club CASCADE;
DROP TABLE IF EXISTS athlete CASCADE;
DROP TABLE IF EXISTS meet CASCADE;
DROP TABLE IF EXISTS fact CASCADE;

CREATE TABLE swimstyle(
    swimstyleid     INT NOT NULL,
    distance        INT,
    stroke          VARCHAR(25),
    relaycount      VARCHAR(25),

    PRIMARY KEY(swimstyleid) 
);

CREATE TABLE club(
    clubid          INT NOT NULL,
    code            VARCHAR(25),
    name            VARCHAR(50),
    nation          VARCHAR(25),
    region          VARCHAR(25),
    PRIMARY KEY(clubid) 
);


CREATE TABLE athlete(
    athleteid       INT NOT NULL,
    completeName    VARCHAR(50),
    nation          VARCHAR(25),
    birthdate       VARCHAR(25),
    license         VARCHAR(25),
    gender          VARCHAR(25),

    PRIMARY KEY(athleteid) 
);

CREATE TABLE meet(
    meetid          INT NOT NULL,
    city            VARCHAR(25),
    name            VARCHAR(75),
    organizer       VARCHAR(50),  
    number          INT,
    dateStart       DATE,        
    dateEnd         DATE, 
    course          VARCHAR(25), 
    PRIMARY KEY(meetid) 
);

INSERT INTO swimstyle(swimstyleid, distance, stroke, relaycount) 
    SELECT swimstyleid, distance::INT, stroke, relaycount FROM old_swimstyle;

INSERT INTO club(clubid, code, name, nation, region) 
    SELECT clubid, code, name, nation, region FROM old_club;

INSERT INTO athlete(athleteid, completeName, nation, birthdate, license,gender) 
    SELECT athleteid, concat(firstname, ' ', lastname) as name, nation, birthdate , license, gender FROM old_athlete;

INSERT INTO meet(meetid, city, name, organizer, number, course)
    SELECT meetid, city, name, organizer, number::INT, course FROM old_meet;

/* TODO: Preencher depois
INSERT INTO db_datawarehousing.meet(meetid, dateStart, dateEnd) 
    SELECT old_meet.meetid, MIN(date), MAX(date) FROM old_session, old_meet where db_datawarehousing.meet.meetid = old_session.meetid GROUP BY old_session.meetid;*/

CREATE TABLE fact(
    athleteid   INT,    
    swimstyleid INT,   
    clubid      INT,   
    meetid      INT,   
    
    swimTime    VARCHAR(25), /*Vem do result*/
    points      INT, /*Vem do result*/

    FOREIGN KEY (athleteid) REFERENCES athlete(athleteid),
    FOREIGN KEY (swimstyleid) REFERENCES swimstyle(swimstyleid),
    FOREIGN KEY (clubid) REFERENCES club(clubid),
    FOREIGN KEY (meetid) REFERENCES meet(meetid)
);

/*
INSERT INTO fact(athleteid, clubid, meetid, swimstyleid, poolName, swimTime, points) 
    SELECT old_athleteid, old_clubid, old_meetid, old_swimstyleid , pool.name, result.swimTime, result.points
    FROM old_athlete, old_club, old_meet, old_swimstyle, old_event, old_session , old_pool, old_result
    WHERE athlete.clubid = club.clubid and club.meetid = meet.meetid and 
    swimstyle.eventid = event.eventid and event.sessionid = session.sessionid and session.meetid = meet.meetid and pool.meetid =meet.meetid and result.athleteid = athlete.athleteid
;
*/

INSERT INTO fact(athleteid, clubid, meetid, swimstyleid, swimTime, points) 
    SELECT old_athlete.athleteid, old_club.clubid, old_meet.meetid, old_swimstyle.swimstyleid, old_result.swimTime, old_result.points
    FROM old_athlete, old_club, old_meet, old_swimstyle, old_event, old_session , old_pool, old_result
    WHERE old_athlete.clubid = old_club.clubid and old_club.meetid = old_meet.meetid and 
    old_swimstyle.eventid = old_event.eventid and old_event.sessionid = old_session.sessionid and old_session.meetid = old_meet.meetid and old_result.athleteid = old_athlete.athleteid and old_result.eventid = old_event.eventid;
;
