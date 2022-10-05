import sqlite3
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("lib.sqlite")
# создаем таблицу, если ее еще не было, заносим в нее записи
con.executescript('''
DROP TABLE IF EXISTS publisher;
CREATE TABLE IF NOT EXISTS publisher(
publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
publisher_name VARCHAR(60)
);
DROP TABLE IF EXISTS book;
CREATE TABLE IF NOT EXISTS book(
book_id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(60),
genre_id INTEGER,
publisher_id INTEGER,
year_publication INTEGER,
available_numbers INTEGER,
FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);
INSERT INTO publisher (publisher_name)
VALUES
('ЭКСМО'),
('ДРОФА'),
('АИСТ');
INSERT INTO book (title, genre_id, publisher_id, year_publication, available_numbers)
VALUES
("Мастер и Маргарита", 1, 2, 2014, 5),
("Таинственный остров", 2, 2, 2015, 10),
("Бородино", 7, 3, 2015, 12),
("Дубровский", 1, 2, 2020, 7),
("Вокруг свет за 80 дней", 2, 2, 2019, 5),
("Убийства по алфавиту", 1, 1, 2017, 9),
("Затерянный мир", 2, 1, 2020, 3),
("Герой нашего времени", 1, 3, 2017, 2),
("Смерть поэта", 7, 1, 2020, 2),
("Поэмы", 7, 3, 2019, 5);
''')