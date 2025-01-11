
--Documentation:
--Author: Karuna Motiram Ravate
--Date: January 6, 2025
--Description:
--This SQL code sets up a comprehensive system for managing study plans, sessions, and progress tracking. It includes user management, study plans, session scheduling, and progress tracking with stored procedures, functions, and triggers.


-- Table: Users
CREATE TABLE Users (
    UserID NUMBER PRIMARY KEY,
    UserName VARCHAR2(50),
    Password VARCHAR2(50),
    Email VARCHAR2(100),
    CreatedDate DATE DEFAULT SYSDATE
);

-- Table: Subjects
CREATE TABLE Subjects (
    SubjectID NUMBER PRIMARY KEY,
    UserID NUMBER,
    SubjectName VARCHAR2(100),
    HoursPerWeek NUMBER,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Table: StudyPlans
CREATE TABLE StudyPlans (
    PlanID NUMBER PRIMARY KEY,
    UserID NUMBER,
    StartDate DATE,
    EndDate DATE,
    Goal VARCHAR2(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Table: StudySessions
CREATE TABLE StudySessions (
    SessionID NUMBER PRIMARY KEY,
    PlanID NUMBER,
    SessionDate DATE,
    SubjectName VARCHAR2(100),
    DurationInHours NUMBER,
    Status VARCHAR2(20) DEFAULT 'Scheduled',
    FOREIGN KEY (PlanID) REFERENCES StudyPlans(PlanID)
);

-- Table: Progress
CREATE TABLE Progress (
    ProgressID NUMBER PRIMARY KEY,
    UserID NUMBER,
    PlanID NUMBER,
    SessionID NUMBER,
    Completed NUMBER(1) DEFAULT 0,
    CompletionDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (PlanID) REFERENCES StudyPlans(PlanID),
    FOREIGN KEY (SessionID) REFERENCES StudySessions(SessionID)
);

-- Procedure: GenerateStudyPlan
CREATE OR REPLACE PROCEDURE GenerateStudyPlan (
    p_userid IN NUMBER,
    p_start_date IN DATE,
    p_end_date IN DATE,
    p_goal IN VARCHAR2
) AS
BEGIN
    INSERT INTO StudyPlans (UserID, StartDate, EndDate, Goal)
    VALUES (p_userid, p_start_date, p_end_date, p_goal);
END;

-- Function: CalculateCompletedSessions
CREATE OR REPLACE FUNCTION CalculateCompletedSessions (
    p_planid IN NUMBER
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM Progress
    WHERE PlanID = p_planid AND Completed = 1;
    
    RETURN v_count;
END;
/

-- Trigger: UpdateProgressAfterSession
CREATE OR REPLACE TRIGGER UpdateProgressAfterSession
AFTER INSERT ON StudySessions
FOR EACH ROW
DECLARE
    v_userid NUMBER;
BEGIN
    SELECT UserID INTO v_userid
    FROM StudyPlans
    WHERE PlanID = :NEW.PlanID;

    INSERT INTO Progress (UserID, PlanID, SessionID, Completed, CompletionDate)
    VALUES (v_userid, :NEW.PlanID, :NEW.SessionID, 0, NULL);
END;
/

--insert a user
INSERT INTO Users (UserID, UserName)
VALUES (1, 'John Doe');

----generate a stuudy plan
CALL GenerateStudyPlan(1, TO_DATE('2025-01-10', 'YYYY-MM-DD'), TO_DATE('2025-03-10', 'YYYY-MM-DD'), 'Complete Semester 1 Syllabus');
----insert study session
INSERT INTO StudySessions (SessionID, PlanID, SessionDate, SubjectName, DurationInHours)
VALUES (301, 101, TO_DATE('2025-02-01', 'YYYY-MM-DD'), 'History', 3);
