import sqlite3
import pandas as pd
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("library.sqlite")
df = pd.read_sql('''
SELECT title Название,genre_name Жанр, year_publication Год,
    (CASE
        WHEN year_publication < 2014
            THEN 'III'
        WHEN year_publication >= 2014 and year_publication <= 2017
            THEN 'II'
        WHEN year_publication > 2017
            THEN 'I'
    END) Группа
FROM book
JOIN genre USING (genre_id)
JOIN publisher USING (publisher_id)
WHERE publisher_name = :publisher
ORDER BY Группа DESC, year_publication, title
''', con, params={"publisher": "РОСМЭН"})
print(df)
# закрываем соединение с базой
con.close()