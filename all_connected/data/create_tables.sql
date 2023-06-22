USE snapngo_db;

DROP TABLE IF EXISTS `assignments`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `tasks`;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50),
    `name` VARCHAR(50),
    compensation DECIMAL(4,2) DEFAULT 0,
    reliability DECIMAL(4,2) DEFAULT NULL,
    PRIMARY KEY (id)
)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT,
    `location` VARCHAR(100),
    `description` VARCHAR(100),
    start_time DATETIME,
    deadline DATETIME,
    time_window INT(3),
    compensation DECIMAL(4,2) DEFAULT 0,
    expired BOOLEAN,
    PRIMARY KEY (id)
)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT,
    task_id INT,
    user_id VARCHAR(15),
    recommend_time DATETIME,
    img varchar(100),
    submission_time DATETIME,
    `status` ENUM('not assigned','accepted','rejected','pending') DEFAULT 'not assigned',
    PRIMARY KEY (id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
)
ENGINE = InnoDB;

    
