CREATE TABLE IF NOT EXISTS `user` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `username` TEXT NOT NULL,
    `role` TEXT NOT NULL,
    `reg_date` TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS `book` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL,
    `authors` TEXT NOT NULL,
    `price` REAL NOT NULL,
    `length` INTEGER NOT NULL,
    `is_available` BOOL NOT NULL,
    `source` BLOB NOT NULL,
    `image` BLOB,
    `recieve_date` TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS `genre` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `book_genre` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `book_id` INTEGER NOT NULL,
    `genre_id` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `order` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER NOT NULL,
    `datetime` TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS `order_book` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `order_id` INTEGER NOT NULL,
    `book_id` INTEGER NOT NULL,
    `quantity` INTEGER NOT NULL
);

ALTER TABLE `book_genre` ADD FOREIGN KEY (`book_id`) REFERENCES `book`(`id`);
ALTER TABLE `book_genre` ADD FOREIGN KEY (`genre_id`) REFERENCES `genre`(`id`);
ALTER TABLE `order` ADD FOREIGN KEY (`user_id`) REFERENCES `user`(`id`);
ALTER TABLE `order_book` ADD FOREIGN KEY (`order_id`) REFERENCES `order`(`id`);
ALTER TABLE `order_book` ADD FOREIGN KEY (`book_id`) REFERENCES `book`(`id`);