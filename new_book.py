import sqlite3
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("lib.sqlite")
# создаем таблицу, если ее еще не было, заносим в нее записи
con.executescript('''
DROP TABLE IF EXISTS genre;

CREATE TABLE IF NOT EXISTS genre(
genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
genre_name VARCHAR(30)
);

INSERT INTO genre (genre_name)
VALUES
('Роман'),
('Приключения'),
('Детектив'),
('Лирика'),
('Фантастика'),
('Фэнтэзи'),
('Поэзия');

DROP TABLE IF EXISTS publisher;
CREATE TABLE IF NOT EXISTS publisher(
publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
publisher_name VARCHAR(60)
);

DROP TABLE IF EXISTS new_book;
CREATE TABLE IF NOT EXISTS new_book(
book_id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(60),
publisher_name INTEGER,
year_publication VARCHAR(60),
amount INTEGER
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

INSERT INTO new_book(title, publisher_name, year_publication, amount)
VALUES
('Вокруг света за 80 дней', 'ДРОФА', 2019, 2),
('Собачье сердце', 'АСТ', 2020, 3),
('Таинственный остров','РОСМЭН', 2015, 1),
('Евгений Онегин', 'АЛЬФА-КНИГА', 2020, 4),
('Герой нашего времени', 'АСТ', 2017, 1);
''')
con.commit()
cursor = con.cursor()
cursor.execute('''
SELECT * FROM book
''')
print(cursor.fetchall())
cursor.execute('''
UPDATE book
SET available_numbers = available_numbers + (
SELECT amount FROM book
JOIN genre USING (genre_id)
JOIN new_book b USING (title)
)
WHERE
(SELECT title FROM book
JOIN publisher USING (publisher_id)
JOIN new_book USING (title)
WHERE new_book.title = book.title
AND new_book.publisher_name = publisher.publisher_name
AND new_book.year_publication = book.year_publication)
''')
cursor.execute('''
SELECT title, (SELECT publisher_name FROM publisher 
JOIN new_book USING (publisher_name)
) FROM book
JOIN new_book USING (title)
JOIN publisher USING (publisher_name)
WHERE new_book.title = book.title
AND new_book.year_publication = book.year_publication
AND new_book.publisher_name = publisher.publisher_name
''')
cursor.execute('''
SELECT title, (SELECT publisher_name FROM publisher 
JOIN new_book USING (publisher_name)
)
FROM book
''')
print(cursor.fetchall())
cursor.execute('''
SELECT title, publisher_name FROM new_book
JOIN publisher USING (publisher_name)
WHERE new_book.publisher_name = publisher.publisher_name
''')
print(cursor.fetchall())
con.close()