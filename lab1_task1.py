import sqlite3
import pandas as pd
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
con.commit()
cursor = con.cursor()
cursor.execute('''
SELECT title, genre_name FROM book
JOIN genre USING (genre_id)
WHERE available_numbers BETWEEN :a AND :b
''', {"a": 2, "b": 10})
print(cursor.fetchall())
cursor = con.cursor()
cursor.execute('''
SELECT title, publisher_name FROM book
JOIN publisher USING (publisher_id)
WHERE title NOT LIKE '% %' AND book.year_publication > :year
''',{"year" :2017})
print(cursor.fetchall())
cursor = con.cursor()
cursor.execute('''
SELECT title, genre_name, sum(available_numbers) FROM book
JOIN genre USING (genre_id)
WHERE year_publication > :year
GROUP BY genre_id
''',{"year" :2017})
print(cursor.fetchall())
df = pd.read_sql('''
    SELECT book.title Книга, genre.genre_name Жанр, publisher.publisher_name Издательство, book.available_numbers Количество
    FROM book
    JOIN genre USING(genre_id)
    JOIN publisher USING(publisher_id)
    WHERE book.available_numbers>3''', con)
print(df)

publishers=("ДРОФА", "ЭКСМО")
df=pd.read_sql(f'''
    SELECT title Название FROM book 
    JOIN publisher 
    ON publisher.publisher_id=book.publisher_id
    WHERE publisher.publisher_name IN {publishers}
    AND
    book.year_publication BETWEEN 2016 and 2019
''', con)
print(df)
# закрываем соединение с базой
con.close()