USE crowdnets_db;

-- create a table for the users
CREATE TABLE 'users' (
    'id' VARCHAR(50),
    'name' VARCHAR(50),
    'compensation' DECIMAL(4,2),
    'reliability' DECIMAL(4,2),
    PRIMARY KEY ('id')
)
-- table constraint
ENGINE = InnoDB;

-- create a table for the tasks
CREATE TABLE 'tasks' (
    'id' INT AUTO_INCREMENT,
    'location' VARCHAR(100),
    'description' VARCHAR(100),
    'deadline' DATETIME,
    'window' INT(3),
    'compensation' DECIMAL(4,2),
    'expired' BOOLEAN,
    PRIMARY KEY ('id')
)
-- table constraint
ENGINE = InnoDB;

-- create a table for the assignments
CREATE TABLE assignments (
    taskID INT,
    userID VARCHAR(15),
    recommendTime DATETIME, -- when recommended
    img BLOB,
    submissionTime DATETIME,
    accepted BIT,
    PRIMARY KEY (taskID, userID),
    FOREIGN KEY (taskID) REFERENCES 'tasks'('id')
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (userID) REFERENCES 'users'('id')
        ON UPDATE CASCADE
        ON DELETE SET NULL
)
-- table constraint
ENGINE = InnoDB;
    
