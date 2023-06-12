USE snapngo_db;


CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50),
    `name` VARCHAR(50),
    compensation DECIMAL(4,2) DEFAULT 0,
    reliability DECIMAL(4,2),
    PRIMARY KEY (id)
)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT,
    location VARCHAR(100),
    `description` VARCHAR(100),
    deadline DATETIME,
    `time_window` INT(3),
    compensation DECIMAL(4,2),
    expired BOOLEAN,
    PRIMARY KEY (id)
)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS assignments (
    id INT,
    taskID INT,
    userID VARCHAR(15),
    recommendTime DATETIME,
    img BLOB,
    submissionTime DATETIME,
    status ENUM('not assigned','accepted','rejected','pending'),
    PRIMARY KEY (id),
    FOREIGN KEY (taskID) REFERENCES tasks(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
ENGINE = InnoDB;

ALTER TABLE tasks ADD COLUMN starttime DATETIME;
    
