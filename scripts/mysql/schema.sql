DROP TABLE IF EXISTS `elt`;
CREATE TABLE IF NOT EXISTS `elt` 
(
    `track_id` INT NOT NULL,
    `cars` TEXT NOT NULL,
    `traveled_d` FLOAT NOT NULL,
    `avg_speed` FLOAT NOT NULL,
    `lat` FLOAT NOT NULL,
    `lon` FLOAT NOT NULL,
    `speed` FLOAT NOT NULL,
    `lon_acc` FLOAT NOT NULL,
    `lat_acc` FLOAT NOT NULL,
    `time` FLOAT NOT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
